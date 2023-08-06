from __future__ import annotations
from typing import Generic, List, Type, TypeVar, TYPE_CHECKING

from taipan_di.classes.tools import ChainOfResponsibilityLink, ChainOfResponsibilityFactory
from taipan_di.errors import TaipanRegistrationError
from taipan_di.interfaces import BaseDependencyProvider

from taipan_di.classes import instanciate_service

if TYPE_CHECKING:
    from taipan_di.classes import DependencyCollection

__all__ = ["ChainOfResponsibilityRegistrator"]

T = TypeVar("T")
U = TypeVar("U")


class ChainOfResponsibilityRegistrator(Generic[T, U]):
    def __init__(
        self,
        interface_type: Type[ChainOfResponsibilityLink[T, U]],
        services: DependencyCollection,
        as_singleton=False,
    ) -> None:
        self._interface_type = interface_type
        self._services = services
        self._as_singleton = as_singleton
        self._link_types: List[Type[ChainOfResponsibilityLink[T, U]]] = []

    def add(
        self, link: Type[ChainOfResponsibilityLink[T, U]]
    ) -> ChainOfResponsibilityRegistrator[T, U]:
        self._link_types.append(link)
        return self

    def register(self) -> None:
        if len(self._link_types) == 0:
            raise TaipanRegistrationError(
                f"Pipeline[{str(T)}, {str(U)}] is empty ! Add at least one link"
            )

        def create_chain_of_responsibility(
            provider: BaseDependencyProvider,
        ) -> ChainOfResponsibilityLink[T, U]:
            factory = ChainOfResponsibilityFactory[T, U]()

            for link_type in self._link_types:
                link = instanciate_service.instanciate_service(link_type, provider)
                factory.add(link)

            return factory.build()

        if self._as_singleton:
            self._services.register_singleton_creator(
                self._interface_type, create_chain_of_responsibility
            )
        else:
            self._services.register_factory_creator(
                self._interface_type, create_chain_of_responsibility
            )
