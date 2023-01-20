from typing import Dict, Any

from amir_dev_studio.dependency_injection.providers import Singleton, Transient, BaseProvider

_provider_container: Dict[Any, BaseProvider] = {}


def _add_service_to_container(key, value: BaseProvider):
    if key in _provider_container:
        raise ValueError(f'Key {key} already exists in the container')
    _provider_container[key] = value


def get_service(key):
    if key not in _provider_container:
        raise ValueError(f'Key {key} does not exist in the container')
    return _provider_container[key].get_service()


def add_singleton_service(service_class, service_init_args=None, service_init_kwargs=None):
    _add_service_to_container(
        service_class,
        Singleton(
            service_class,
            service_init_args,
            service_init_kwargs,
        )
    )


def add_transient_service(service_class, service_init_args=None, service_init_kwargs=None):
    _add_service_to_container(
        service_class,
        Transient(
            service_class,
            service_init_args,
            service_init_kwargs,
        )
    )


def add_abstract_transient_service(abstract_class, concrete_class, service_init_args=None, service_init_kwargs=None):
    _add_service_to_container(
        abstract_class,
        Transient(
            concrete_class,
            service_init_args,
            service_init_kwargs,
        )
    )


def add_abstract_singleton_service(abstract_class, concrete_class, service_init_args=None, service_init_kwargs=None):
    _add_service_to_container(
        abstract_class,
        Singleton(
            concrete_class,
            service_init_args,
            service_init_kwargs,
        )
    )


def add_named_singleton_service(name, service_class, service_init_args=None, service_init_kwargs=None):
    _add_service_to_container(
        name,
        Singleton(
            service_class,
            service_init_args,
            service_init_kwargs,
        )
    )


def add_named_transient_service(name, service_class, service_init_args=None, service_init_kwargs=None):
    _add_service_to_container(
        name,
        Transient(
            service_class,
            service_init_args,
            service_init_kwargs
        )
    )
