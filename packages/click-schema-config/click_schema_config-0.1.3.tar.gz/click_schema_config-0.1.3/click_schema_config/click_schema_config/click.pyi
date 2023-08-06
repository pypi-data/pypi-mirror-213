from .types import FileLike as FileLike
from click.decorators import FC as FC
from typing import Any, Protocol

class Decorator(Protocol):
    def __call__(self, func: FC) -> FC: ...

def schema_from_inis(files: list[FileLike] | FileLike = ..., insecure_eval: bool = ..., **kwargs: Any) -> Decorator: ...
