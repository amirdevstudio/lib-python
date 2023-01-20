import logging
from abc import ABC, abstractmethod
from logging import Logger
from threading import Lock


class AbstractExecutor(ABC):
    def __init__(self, logger: Logger = None):
        self._lock = Lock()
        self._logger = logger or logging.getLogger(__name__)

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...
