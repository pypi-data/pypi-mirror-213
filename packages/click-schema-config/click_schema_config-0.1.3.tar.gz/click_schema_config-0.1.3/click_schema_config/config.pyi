from typing import Any, Iterable

from dataclasses import dataclass

@dataclass
class Variable:
    type: str | None = None
    value: Any | None = None
    description: str | None = None
    required: bool = False


Section = dict[str, Variable]
Config = dict[str, Section]


FileLike = Iterable[str] | str

def read_config(config: FileLike, preconfig: Config | None = ...) -> Config: ...
def read_configs(filenames: FileLike | list[FileLike], preconfig: Config | None = ...) -> Config: ...
