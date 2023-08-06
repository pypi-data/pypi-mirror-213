from typing import Any, Protocol, Iterable
from click.decorators import FC
FileLike = Iterable[str] | str

class Decorator(Protocol):
    def __call__(self, func: FC) -> FC: ...

def schema_from_inis(files: list[FileLike] | FileLike = ..., insecure_eval: bool = ..., **kwargs: Any) -> Decorator: ...
