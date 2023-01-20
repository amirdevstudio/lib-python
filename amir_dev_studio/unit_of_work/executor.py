from abc import ABC, abstractmethod
from logging import Logger, getLogger
from threading import Lock

_default_logger = getLogger(__name__)


class AbstractExecutor(ABC):
    def __init__(self, logger: Logger = _default_logger):
        self._lock = Lock()
        self._logger = logger

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...
