"""
Asynchronous high-level communication with BitTorrent clients
"""

__version__ = '1.1.3'

# isort:skip_file

from .clients import APIBase
from .clients import DelugeAPI, QbittorrentAPI, RtorrentAPI, TransmissionAPI
from .response import Response
from .errors import *  # noqa: F403

from functools import lru_cache as _lru_cache


@_lru_cache
def api_classes():
    """Return sequence of :class:`~.APIBase` subclasses"""
    import inspect

    def is_api_class(obj):
        return (
            inspect.isclass(obj)
            and issubclass(obj, APIBase)
            and obj is not APIBase
        )

    return tuple(
        sorted(
            (cls for cls in globals().values() if is_api_class(cls)),
            key=lambda cls: cls.name
        )
    )


@_lru_cache
def client_names():
    """
    Return sequence of valid client names

    The name of a client is specified by the `name` attribute of the
    :class:`~.APIBase` subclass.
    """
    return tuple(cls.name for cls in api_classes())


def api_class(name):
    """
    Get :class:`~.APIBase` subclass from client name

    :param name: :attr:`~.APIBase.name` of the client to instantiate

    :raise ValueError: if `name` is not a known client name
    """
    for cls in api_classes():
        if cls.name == name:
            return cls
    raise ValueError(f'Unknown client: {name!r}')


def api(name, **kwargs):
    """
    Instantiate :class:`~.APIBase` subclass

    :param name: :attr:`~.APIBase.name` of the client to instantiate
    :param kwargs: Arguments for the :attr:`~.APIBase` subclass

    :raise ValueError: if `name` is not a known client name
    """
    cls = api_class(name)
    return cls(**kwargs)
