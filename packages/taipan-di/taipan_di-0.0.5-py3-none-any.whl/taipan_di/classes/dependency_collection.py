from typing import Callable, Type, TypeVar

from taipan_di.interfaces import BaseDependencyProvider

from .dependency_container import DependencyContainer
from .instanciate_service import instanciate_service
from .scopes import FactoryScope, SingletonScope
from .tools import (
    PipelineLink,
    PipelineRegistrator,
    ChainOfResponsibilityLink,
    ChainOfResponsibilityRegistrator,
)

__all__ = ["DependencyCollection"]

T = TypeVar("T")
U = TypeVar("U")


class DependencyCollection:
    def __init__(self) -> None:
        self._container = DependencyContainer()

    # Public methods

    ## Singleton

    def register_singleton_creator(
        self, type: Type[T], creator: Callable[[BaseDependencyProvider], T]
    ) -> None:
        """
        Registers a service as a singleton by specifying how to create its instance.
        """
        service = SingletonScope(creator)
        self._container.register(type, service)

    def register_singleton_instance(self, type: Type[T], instance: T) -> None:
        """
        Registers a service as a singleton by providing the instance to return.
        """
        creator = lambda provider: instance
        self.register_singleton_creator(type, creator)

    def register_singleton(
        self, interface_type: Type[T], implementation_type: Type[T] = None
    ) -> None:
        """
        Register a service as a singleton by specifying the implementation type to use.

        On resolve, the implementation will be instanciated with its dependencies automatically resolved.

        If the implementation type isn't provided, the interface type will be used as the implementation type.

        If the implementation type don't possess an __init__ method, the resolve will fail.
        """
        if implementation_type is None:
            implementation_type = interface_type

        creator = lambda provider: instanciate_service(implementation_type, provider)
        self.register_singleton_creator(interface_type, creator)

    ## Factory

    def register_factory_creator(
        self, type: Type[T], creator: Callable[[BaseDependencyProvider], T]
    ) -> None:
        """
        Registers a service as a factory by specifying how to create its instances.
        """
        service = FactoryScope(creator)
        self._container.register(type, service)

    def register_factory(
        self, interface_type: Type[T], implementation_type: Type[T] = None
    ) -> None:
        """
        Register a service as a factory by specifying the implementation type to use.

        On resolve, the implementation will be instanciated with its dependencies automatically resolved.

        If the implementation type isn't provided, the interface type will be used as the implementation type.

        If the implementation type don't possess an __init__ method, the resolve will fail.
        """
        if implementation_type is None:
            implementation_type = interface_type

        creator = lambda provider: instanciate_service(implementation_type, provider)
        self.register_factory_creator(interface_type, creator)

    ## Chain of Responsibility

    def register_chain_of_responsibility(
        self, interface_type: Type[ChainOfResponsibilityLink[T, U]], as_singleton=False
    ) -> ChainOfResponsibilityRegistrator[T, U]:
        """
        Initiate the registration of a service as a chain of responsibility.

        Returns a registrator to be used to add the links and then register the service.
        """
        registrator = ChainOfResponsibilityRegistrator[T, U](
            interface_type, self, as_singleton
        )
        return registrator

    ## Pipeline

    def register_pipeline(
        self, interface_type: Type[PipelineLink[T, U]], as_singleton=False
    ) -> PipelineRegistrator[T, U]:
        """
        Initiate the registration of a service as a pipeline.

        Returns a registrator to be used to add the links and then register the service.
        """
        registrator = PipelineRegistrator[T, U](interface_type, self, as_singleton)
        return registrator

    ## Build

    def build(self) -> BaseDependencyProvider:
        """
        Builds the service provider containing the services registered by this collection.
        """
        return self._container.build()
