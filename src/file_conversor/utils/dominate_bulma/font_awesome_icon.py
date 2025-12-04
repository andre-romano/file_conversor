# src\file_conversor\backend\gui\_components\icon.py

from file_conversor.utils.dominate_utils import i, span


def FontAwesomeIcon(
        name: str,
        _class: str = "",
        **kwargs,
):
    """
    Create a FontAwesome icon component.

    :param name: The name of the icon (e.g., "home", "settings").
    :param _class: Additional CSS classes to apply to the icon.
    """
    with span(_class=f"icon {_class}", **kwargs) as component:
        i(_class=f"fas fa-{name}")
    return component


__all__ = ["FontAwesomeIcon"]
