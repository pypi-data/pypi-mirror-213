from typing import Generic, List, TypeVar

from taipan_di.classes.tools import PipelineLink
from taipan_di.errors import TaipanRegistrationError

__all__ = ["PipelineFactory"]

T = TypeVar("T")
U = TypeVar("U")


class PipelineFactory(Generic[T, U]):
    def __init__(self) -> None:
        self._links: List[PipelineLink[T, U]] = []

    def add(self, link: PipelineLink[T, U]) -> "PipelineFactory[T, U]":
        self._links.append(link)
        return self

    def build(self) -> PipelineLink[T, U]:
        if len(self._links) == 0:
            raise TaipanRegistrationError(
                f"Pipeline[{str(T)}, {str(U)}] is empty ! Add at least one link"
            )

        for i in range(len(self._links) - 1):
            self._links[i]._set_next(self._links[i + 1])

        return self._links[0]
