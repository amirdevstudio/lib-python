from abc import ABC, abstractmethod
from threading import Lock

from amir_dev_studio.dependency_injection.globals import (
    default_args, default_kwargs
)


class AbstractProvider(ABC):
    @abstractmethod
    def get_service(self):
        ...


class AbstractServiceClassProvider(AbstractProvider, ABC):
    def __init__(
        self,
        cls: type,
        cls_args: tuple = default_args,
        cls_kwargs: dict = default_kwargs,
    ):
        self._lock = Lock()
        self.cls = cls
        self.cls_args = cls_args
        self.cls_kwargs = cls_kwargs


class Singleton(AbstractServiceClassProvider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = None

    def get_service(self):
        with self._lock:
            if not self.instance:
                self.instance = self.cls(*self.cls_args, **self.cls_kwargs)
        return self.instance


class Transient(AbstractServiceClassProvider):
    def get_service(self):
        with self._lock:
            return self.cls(*self.cls_args, **self.cls_kwargs)
