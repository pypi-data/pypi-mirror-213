from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple


@dataclass
class Func:
    """
    Func is a dataclass that represents a function to be executed as a batch job.

    Attributes
    ----------
    func : Callable[..., Any]
        The function to be executed.
    fargs : Tuple[Any]
        The function's arguments.
    fkwargs : dict[str, Any]
        The function's keyword arguments.
    requirements_path : Optional[str]
        A path to the function's requirements file.
    """

    func: Callable[..., Any]
    fargs: Tuple[Any]
    fkwargs: dict[str, Any]
    requirements_path: Optional[str] = None
