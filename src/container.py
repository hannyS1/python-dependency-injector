import functools
import copy
from typing import List, Callable, Dict, Optional, Iterable

from src.annotations import Annotation, AnnotationManager
from src.enums import ProviderType
from src.interfaces import IContext
from src.providers import IProvider, ProviderFactory


class Container:

    def __init__(self):
        self.providers: List[IProvider] = []
        self.provider_factory = ProviderFactory()

    @staticmethod
    def _get_obj_interface(obj: Callable, interface: Optional[type]):
        if not interface and isinstance(obj, type):
            interface = obj

        if not interface:
            raise Exception('cant define provider interface')

        return interface

    @staticmethod
    def _get_context_instances_from_injected(injected: Dict[str, object]) -> Iterable[IContext]:

        def find_context_instances():
            for injected_instance in injected.values():
                if isinstance(injected_instance, IContext) or hasattr(injected_instance, 'on_enter') \
                        and hasattr(injected_instance, 'on_exit'):
                    yield injected_instance

        return find_context_instances()

    def _check_existing_interfaces(self, interface: type):
        for provider in self.providers:
            if provider.check_interface(interface):
                raise Exception('interface already exist')

    def register(self, obj: Callable, provider_type: ProviderType = ProviderType.FACTORY,
                 interface: type = None) -> IProvider:

        interface = self._get_obj_interface(obj, interface)
        self._check_existing_interfaces(interface)
        provider = self.provider_factory.create(obj, provider_type, interface)
        self.providers.append(provider)
        return provider

    def component(self, provider_type: ProviderType = ProviderType.FACTORY, interface: type = None):

        def decorator(obj: Callable):
            self.register(obj, provider_type, interface)
            return obj

        return decorator

    def autowired(self, func):
        local_providers = copy.copy(self.providers)
        annotations: List[Annotation] = AnnotationManager.from_dict(func.__annotations__)
        to_inject: Dict[str, object] = {}
        for annotation in annotations:
            for provider in local_providers:
                if provider.check_interface(annotation.interface):
                    to_inject[annotation.name] = provider.get_instance()
                    local_providers.remove(provider)
                    continue

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            context_instances: List[IContext] = list(self._get_context_instances_from_injected(to_inject))

            for context_instance in context_instances:
                context_instance.on_enter()

            result = func(*args, **to_inject, **kwargs)

            for context_instance in context_instances:
                context_instance.on_exit()

            return result

        return wrapper
