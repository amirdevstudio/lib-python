from threading import Lock
from typing import Dict, Any, TypeVar, Type

from amir_dev_studio.dependency_injection.providers import (
    AbstractProvider,
    Singleton,
    Transient
)

_ArgumentNotSpecified = object()
_default_args = ()
_default_kwargs = {}
_default_namespace = 'default'
_provider_registry: Dict[str, Dict[Type, AbstractProvider]] = {}
_T = TypeVar('_T')
_thread_lock = Lock()


def _add_service_to_registry(
        service_class: Type,
        provider: AbstractProvider,
        namespace: str = _default_namespace
) -> None:
    if namespace in _provider_registry and service_class in _provider_registry[namespace]:
        raise Exception(f"Service already exists for the given class: {service_class} (namespace: {namespace})")

    with _thread_lock:
        if namespace not in _provider_registry:
            _provider_registry[namespace] = {}

        _provider_registry[namespace][service_class] = provider


def get_service(
        service_class: Type,
        default: Any = _ArgumentNotSpecified,
        namespace: str = _default_namespace
) -> _T:
    if namespace not in _provider_registry or service_class not in _provider_registry[namespace]:
        if default is not _ArgumentNotSpecified:
            return default

        raise Exception(f"No service was found for the given class: {service_class} (namespace: {namespace})")

    return _provider_registry[namespace][service_class].get_service()


def add_singleton_service(
        service_class,
        service_init_args: tuple = _default_args,
        service_init_kwargs: dict = _default_kwargs,
        namespace: str = _default_namespace,
):
    _add_service_to_registry(
        service_class,
        Singleton(
            service_class,
            service_init_args,
            service_init_kwargs,
        ),
        namespace
    )


def add_transient_service(
        service_class,
        service_init_args: tuple = _default_args,
        service_init_kwargs: dict = _default_kwargs,
        namespace: str = _default_namespace,
):
    _add_service_to_registry(
        service_class,
        Transient(
            service_class,
            service_init_args,
            service_init_kwargs,
        ),
        namespace
    )


def add_abstract_singleton_service(
        abstract_class,
        concrete_class,
        service_init_args: tuple = _default_args,
        service_init_kwargs: dict = _default_kwargs,
        namespace: str = _default_namespace,
):
    _add_service_to_registry(
        abstract_class,
        Singleton(
            concrete_class,
            service_init_args,
            service_init_kwargs,
        ),
        namespace
    )


def add_abstract_transient_service(
        abstract_class,
        concrete_class,
        service_init_args: tuple = _default_args,
        service_init_kwargs: dict = _default_kwargs,
        namespace: str = _default_namespace,
):
    _add_service_to_registry(
        abstract_class,
        Transient(
            concrete_class,
            service_init_args,
            service_init_kwargs,
        ),
        namespace
    )
