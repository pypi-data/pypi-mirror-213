"""utils.py."""

import ast
import base64
import inspect
import json
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Callable, Optional

import dill
import requests

from strangeworks_core.errors.error import StrangeworksError
from strangeworks_core.platform.gql import API, APIInfo, Operation
from strangeworks_core.types.func import Func
from strangeworks_core.types.machine import Accelerator, Machine


def send_batch_request(
    api: API,
    batch_job_init_create: Operation,
    decorator_name: str,
    func: Func,
    machine: Optional[Machine] = None,
    accelerator: Optional[Accelerator] = None,
    **kwargs,
) -> str:
    """Send batch request.

    Sends an initiate request to the platform to create a batch job.
    Packages up the user program and any requirements
    and stores them where the platform needs them to be.
    Sends a finalize request to the platform to finalize the batch job.



    Parameters
    ----------
    api : API
        API instance.
    batch_job_init_create : Operation
        Operation instance.
    decorator_name : str
        Decorator name.
    func : Func
        Func instance.
    machine : Optional[Machine], optional
        Machine instance, by default None
    accelerator : Optional[Accelerator], optional
        Accelerator instance, by default None
    **kwargs
        Keyword arguments.

    Returns
    -------
    batch_job_slug : str
        Batch job slug.

    Raises
    ------
    StrangeworksError
        Unable to create a batch job for any reason.
    """

    operations = {
        APIInfo.SDK: Operation(
            query="""
            mutation batchJobFinalizeCreate(
                $final: FinalizeBatchJobCreateInput!
            ) {
                batchJobFinalizeCreate(
                    input: $final
                ) {
                    batchJobSlug
                }
            }
            """
        ),
        APIInfo.PRODUCT: Operation(
            query="""
            mutation batchJobFinalizeCreate(
                $final: FinalizeBatchJobCreateInput!
                $resource_slug: String!
                $workspace_member_slug: String
            ){
                batchJobFinalizeCreate(
                    input: {
                        finalize: $final
                        resourceSlug: $resource_slug
                        workspaceMemberSlug: $workspace_member_slug
                    }
                ) {
                    batchJobSlug
                }
            }
            """
        ),
    }

    op = operations.get(api.info, None)
    if not op:
        raise StrangeworksError("api.info not supported for batch job creation")

    try:
        program = _get_user_program(decorator_name, func)
    except Exception as e:
        raise StrangeworksError("unable to get user program") from e

    with tempfile.NamedTemporaryFile(mode="rb+") as tmp:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as archive:
            with archive.open("program.json", "w") as f:
                p = json.dumps(program)
                f.write(p.encode("utf-8"))

            if func.requirements_path:
                try:
                    req_file = open(func.requirements_path, "rb")
                except IOError as e:
                    raise StrangeworksError(message=f"unable to open file: {str(e)}")
                else:
                    with archive.open("requirements.txt", "w") as r:
                        with req_file:
                            r.write(req_file.read())
        tmp.seek(0)
        p = Path(tmp.name)
        stats = p.stat()
        meta_size = stats.st_size
        init = {
            "program": {
                "EntryPoint": func.func.__name__,
                "Language": "python",
                "LanguageVersion": "3.10",
            },
            "fileName": "package.zip",
            "contentType": "application/zip",
            "metaFileType": "zip",
            "metaFileSize": meta_size,
        }

        initial_res = api.execute(batch_job_init_create, init=init, **kwargs)
        init_create = initial_res.get("batchJobInitiateCreate", None)
        if not init_create:
            raise StrangeworksError(
                "unable to create batch job: batchJobInitiateCreate missing in response"
            )

        batch_job_slug = init_create.get("batchJobSlug", None)
        signed_url = init_create.get("signedURL", None)

        if not batch_job_slug or not signed_url:
            raise StrangeworksError(
                """
                unable to create batch job:
                batchJobSlug or signedURL missing in response
                """
            )

        res = requests.put(
            signed_url, data=tmp, headers={"Content-Type": "application/zip"}
        )
        res.raise_for_status()

    if not machine:
        machine = Machine()

    final = {
        "batchJobSlug": batch_job_slug,
        "machine": {
            "Type": machine.type,
            "CPU": machine.cpu,
            "Memory": machine.memory,
        },
    }
    if accelerator:
        final["machineAccelerator"] = {
            "Type": accelerator.type,
            "Count": accelerator.count,
        }
    res = api.execute(
        op,
        final=final,
        **kwargs,
    )
    final_create = res.get("batchJobFinalizeCreate", None)
    if not final_create:
        raise StrangeworksError(
            "unable to finalize batch job: batchJobFinalizeCreate missing in response"
        )
    batch_job_slug = final_create.get("batchJobSlug", None)
    if not batch_job_slug:
        raise StrangeworksError("unable to finalize batch job: batchJobSlug missing")

    return batch_job_slug


def _get_user_program(
    decorator_name: str,
    f: Func,
) -> dict[str, Any]:
    """Create a dictionary of the user program that the batch job recognizes.

    Parameters
    ----------
    decorator_name: str
        The name of the strangeworks decorator to remove from func.
    func: Callable[..., Any]
        The function to create a batch job package for.
    *fargs: Any
        The positional arguments to the function.
    **fkwargs: Any
        The keyword arguments to the function.

    Returns
    -------
    program: dic[str, Any]
        The user program that defines:
        * the entry point
        * the imports
        * the source code
        * the user defined functions
        * the inputs

    Raises
    ------
    StrangeworksError
        If the source file for the function cannot be found.

    """

    file_path = inspect.getsourcefile(f.func)
    if not file_path:
        raise StrangeworksError("Unable to find source file for function.")

    imports = _get_imports(file_path)
    source = _get_source(f.func, decorator_name)
    inputs = _package_fargs_and_fkwargs(*f.fargs, **f.fkwargs)
    user_defined_helper_fns = _user_defined_functions_in_file(
        f.func.__module__, file_path, source
    )
    entry_point = f.func.__name__

    program = {
        "entry_point": entry_point,
        "imports": base64.b64encode(dill.dumps(imports)).decode(),
        "source": base64.b64encode(dill.dumps(source)).decode(),
        "user_defined_functions": base64.b64encode(
            dill.dumps(user_defined_helper_fns)
        ).decode(),
        "inputs": inputs,
        "custom_requirements": f.requirements_path is not None,
    }

    return program


def _get_imports(file_path: str) -> list[str]:
    """Get a list of the imports in a file.

    Parameters
    ----------
    file_path: str
        The path to the file of the function.

    Returns
    -------
    imports: list[str]
        A list of the imports in the file.
    """
    with open(file_path) as f:
        lines = f.readlines()
        return [
            line.strip()
            for line in lines
            if line.startswith("import") or line.startswith("from")
        ]


def _get_source(f: Callable[..., Any], decorator_name: str) -> str:
    """Get the source code of a function, removing the decorator.

    Parameters
    ----------
    f: Callable[..., Any]
        The function to get the source code of.
    decorator_name: str
        The name of the strangeworks decorator to remove from f.

    Returns
    -------
    source_code: str
        The source code of f with the strangeworks batch job decorator removed.

    """

    def _remove_sw_decorator(
        func_name: str, func_source: str, decorator_name: str
    ) -> str:
        """Remove the strangeworks decorator from a function.

        Parameters
        ----------
        func_name: str
            The name of the function that is going to run as a batch job.
        func_source: str
            The source code of the function that is going to run as a batch job.
        decorator_name: str
            The name of the strangeworks decorator to remove from func_source.

        Returns
        -------
        source_code: str
            The source code of the function
            with the strangeworks batch job decorator removed.
        """
        parsed = ast.parse(func_source)
        for node in ast.iter_child_nodes(parsed):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                decorator_index = None
                for index, decorator in enumerate(node.decorator_list):
                    id = None
                    if isinstance(decorator, ast.Call):
                        id = decorator.func.id
                    elif isinstance(decorator, ast.Name):
                        id = decorator.id

                    if id and id == decorator_name:
                        decorator_index = index
                        break
                if decorator_index is not None:
                    node.decorator_list.pop(decorator_index)

                break
        return ast.unparse(parsed)

    return _remove_sw_decorator(f.__name__, inspect.getsource(f), decorator_name)


def _package_fargs_and_fkwargs(*fargs, **fkwargs) -> dict[str, str]:
    """Package the fargs and fkwargs into a dictionary.

    Parameters
    ----------
    *fargs: Any
        The positional arguments to the function.
    **fkwargs: Any
        The keyword arguments to the function.

    Returns
    -------
    fargs_and_fkwargs: dict[str, str]
        keys: "fargs" and "fkwargs"
        values: The base64 encoded dill pickled values of the arguments.

    """
    return {
        "fargs": base64.b64encode(dill.dumps(fargs)).decode(),
        "fkwargs": {
            key: base64.b64encode(dill.dumps(value)).decode()
            for key, value in fkwargs.items()
        },
    }


def _user_defined_functions_in_file(
    func_module: str, func_src_file_path: str, func_source: str
) -> set[str]:
    """Get the source code of all
    user-defined functions in the same file that func_source lives in.

    Parameters
    ----------
    func_module: str
        The name of the module that func_source lives in.
    func_src_file_path: str
        The path to the file that func_source lives in.
    func_source: str
        The source code of the function to get the user-defined functions for.

    Returns
    -------
    user_defined_functions: set[str]
        The source code of all user-defined functions
        in the same file that func_source lives in.

    """
    members = inspect.getmembers(sys.modules[func_module])
    source_for_members_in_user_file = {
        name: inspect.getsource(obj)
        for name, obj in members
        if inspect.isfunction(obj) and inspect.getsourcefile(obj) == func_src_file_path
    }

    visited = set()
    queue = []
    queue.append(func_source)
    visited.add(func_source)

    while queue:
        fn_source = queue.pop(0)
        tree = ast.parse(fn_source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                src_mem = source_for_members_in_user_file.get(node.func.id, None)
                if src_mem and src_mem not in visited:
                    queue.append(src_mem)
                    visited.add(src_mem)

    visited.remove(func_source)
    return visited
