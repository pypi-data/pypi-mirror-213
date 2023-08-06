from typing import Any, Iterable, TypeAlias

from dataclasses import dataclass


@dataclass
class Variable:
    type: str | None = None
    value: Any | None = None
    description: str | None = None
    required: bool = False


Section: TypeAlias = dict[str, Variable]
Config: TypeAlias = dict[str, Section]


FileLike: TypeAlias = Iterable[str] | str
