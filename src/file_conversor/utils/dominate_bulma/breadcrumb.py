# src\file_conversor\backend\gui\_components\breadcrumb.py

from typing import Any

from file_conversor.utils.dominate_bulma.font_awesome_icon import FontAwesomeIcon
from file_conversor.utils.dominate_utils import a, li, nav, ul


def Breadcrumb(*items: dict[str, Any], _class: str = "", **kwargs):
    """
    Create a breadcrumb navigation component.

    :param items: A list of breadcrumb items, each represented as a dictionary with keys.
    :param _class: Additional CSS classes to apply to the breadcrumb container.
    :param kwargs: Additional attributes for the breadcrumb container.

    ```python
    items = [{
        'icon': (Optional) The icon name to display alongside the label
        'label': The display text for the item,
        'url': The URL the item links to,
        'active': A boolean indicating if the item is the current page,
    }]
    ```
    """
    with nav(_class=f"breadcrumb {_class}", _aria_label="breadcrumbs", **kwargs) as component:
        with ul():
            for item in items:
                with li(_class="is-active" if item.get("active") else ""):
                    if item.get("icon"):
                        FontAwesomeIcon(item["icon"])
                    a(item["label"], _href=item["url"])
    return component


__all__ = ["Breadcrumb"]
