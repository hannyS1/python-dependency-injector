from abc import abstractmethod, ABC
from typing import Callable


class IProvider(ABC):

    @abstractmethod
    def __init__(self, obj: Callable, interface: type):
        pass

    @abstractmethod
    def check_interface(self, interface: type) -> bool:
        pass

    @abstractmethod
    def get_instance(self):
        pass


class IContext(ABC):

    @abstractmethod
    def on_enter(self):
        pass

    @abstractmethod
    def on_exit(self):
        pass
