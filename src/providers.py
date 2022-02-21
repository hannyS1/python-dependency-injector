from abc import ABC, abstractmethod
from typing import Callable

from src.enums import ProviderType
from src.interfaces import IProvider


class FactoryProvider(IProvider):

    def __init__(self, obj: Callable, interface: type):
        self.obj = obj
        self.interface = interface

    def check_interface(self, interface: type) -> bool:
        if self.interface == interface or self.obj == interface:
            return True

        return False

    def get_instance(self):
        return self.obj()


class SingletonProvider(IProvider):

    def __init__(self, obj: Callable, interface: type):
        self.obj = obj
        self.interface = interface
        self.instance = None

    def check_interface(self, interface: type) -> bool:
        if self.interface == interface or self.obj == interface:
            return True

        return False

    def get_instance(self):
        if not self.instance:
            self.instance = self.obj()

        return self.instance


class ProviderFactory:

    FACTORY_MAPPING = {
        ProviderType.FACTORY: FactoryProvider,
        ProviderType.SINGLETON: SingletonProvider
    }

    def create(self, obj: Callable, provider_type: ProviderType, interface: type) -> IProvider:
        provider_class = self.FACTORY_MAPPING.get(provider_type)
        return provider_class(obj, interface)
