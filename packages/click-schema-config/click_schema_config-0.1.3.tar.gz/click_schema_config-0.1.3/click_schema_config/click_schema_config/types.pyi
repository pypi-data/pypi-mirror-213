from _typeshed import Incomplete as Incomplete
from typing import Any

class Variable:
    type: str | None
    value: Any | None
    description: str | None
    required: bool
    def __init__(self, type, value, description, required) -> None: ...
Section = dict[str, Variable]
Config = dict[str, Section]
FileLike: Incomplete
