from typing import Any, Iterable

class Variable:
    type: str | None
    value: Any | None
    description: str | None
    required: bool
    def __init__(self, type, value, description, required) -> None: ...
Section = dict[str, Variable]
Config = dict[str, Section]
FileLike: str | Iterable[str]
