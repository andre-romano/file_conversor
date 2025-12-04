# src\file_conversor\utils\bulma\form.py

from typing import Any

from file_conversor.utils.dominate_utils import button, div


def ButtonsContainer(
    *buttons: Any,
    _class: str = "",
    **kwargs,
):
    """
    Create a container for buttons.

    :param buttons: The button elements to include in the container.
    :param _class: Additional CSS classes for the container.
    """
    return div(
        *buttons,
        _class=f"buttons {_class}",
        **kwargs,
    )


def Button(
    *content: Any,
    _class: str = "",
    _type: str = "button",
    _title: str = "",
    **kwargs,
):
    """
    Create a button element.

    :param content: The content for the button. Can be a label, icon element, or other.
    :param _class: Additional CSS classes for the button.
    :param _type: The type attribute for the button.
    :param _title: The help text for the button (used as title attribute).
    """
    return button(
        *[
            c
            for c in content
            if c is not None
        ],
        _class=f"button {_class}",
        _type=_type,
        _title=_title,
        **kwargs,
    )


__all__ = [
    "ButtonsContainer",
    "Button",
]
