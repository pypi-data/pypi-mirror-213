from typing import Generic, List, TypeVar

from taipan_di.classes.tools import ChainOfResponsibilityLink
from taipan_di.errors import TaipanRegistrationError

__all__ = ["ChainOfResponsibilityFactory"]

T = TypeVar("T")
U = TypeVar("U")


class ChainOfResponsibilityFactory(Generic[T, U]):
    def __init__(self) -> None:
        self._links: List[ChainOfResponsibilityLink[T, U]] = []

    def add(
        self, link: ChainOfResponsibilityLink[T, U]
    ) -> "ChainOfResponsibilityFactory[T, U]":
        self._links.append(link)
        return self

    def build(self) -> ChainOfResponsibilityLink[T, U]:
        if len(self._links) == 0:
            raise TaipanRegistrationError(
                f"ChainOfResponsibility[{str(T)}, {str(U)}] is empty ! Add at least one link"
            )

        for i in range(len(self._links) - 1):
            self._links[i]._set_next(self._links[i + 1])

        return self._links[0]
