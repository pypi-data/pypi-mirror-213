from dataclasses import dataclass


@dataclass
class Machine:
    """
    Machine is a dataclass that represents a machine to be used for a batch job.

    Attributes
    ----------
    type : str
        The type of machine to be used.
    cpu : int
        The number of CPUs to be used.
    memory : int
        The amount of memory to be used.
    """

    type: str = "e2-standard-4"
    cpu: int = 1
    memory: int = 1024


@dataclass
class Accelerator:
    """
    Accelerator is a dataclass that represents an accelerator
    that can be used for a batch job.

    Attributes
    ----------
    type : str
        The type of accelerator to be used.
    count : int
        The number of accelerators to be used.
    """

    type: str
    count: int
