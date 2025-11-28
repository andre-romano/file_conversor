# src\file_conversor\utils\flask_utils.py

from typing import Callable

from flask import url_for


def get_url(func_or_endpoint: Callable | str) -> str:
    """
    Gets the URL for a Flask endpoint function.

    :param func_or_endpoint: The Flask endpoint function or endpoint name.
    :return: The URL for the given endpoint.
    """
    if isinstance(func_or_endpoint, str):
        return url_for(func_or_endpoint)
    return url_for(func_or_endpoint.__name__)


__all__ = [
    "get_url",
]
