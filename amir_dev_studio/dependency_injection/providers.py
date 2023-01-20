from abc import ABC, abstractmethod
from threading import Lock


class AbstractProvider(ABC):
    @abstractmethod
    def get_service(self):
        ...


class AbstractServiceClassProvider(ABC, AbstractProvider):
    def __init__(
        self,
        cls,
        cls_args: dict = None,
        cls_kwargs: dict = None,
    ):
        self._lock = Lock()
        self.cls = cls
        self.cls_args = cls_args or ()
        self.cls_kwargs = cls_kwargs or {}


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
