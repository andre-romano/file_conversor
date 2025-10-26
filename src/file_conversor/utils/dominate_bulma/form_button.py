# src\file_conversor\utils\bulma\form.py

from typing import Any

from file_conversor.utils.dominate_utils import *


def Button(
    *content: Any,
    _class: str = "",
    _type: str = "button",
    **kwargs,
):
    """
    Create a button element.

    :param content: The content for the button. Can be a label, icon element, or other.
    :param _class: Additional CSS classes for the button.
    :param _type: The type attribute for the button.
    """
    return button(
        *[
            c
            for c in content
            if c is not None
        ],
        _class=f"button {_class}",
        _type=_type,
        **kwargs,
    )


__all__ = [
    "Button",
]
