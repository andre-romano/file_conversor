# src\file_conversor\utils\bulma\tabs.py

from typing import Any

from file_conversor.utils.dominate_bulma.font_awesome_icon import FontAwesomeIcon

from file_conversor.utils.dominate_utils import *


class TabsAlignment:
    LEFT = "is-left"
    CENTER = "is-centered"
    RIGHT = "is-right"


class TabsSize:
    SMALL = "is-small"
    MEDIUM = "is-medium"
    LARGE = "is-large"


class TabsStyle:
    DEFAULT = ""
    BOXED = "is-boxed"
    TOGGLED = "is-toggle"
    TOGGLED_ROUNDED = "is-toggle is-toggle-rounded"


def Tabs(
    *tabs: dict[str, Any],
    _class: str = "",
    **kwargs,
):
    """
    Create a Bulma tabs component.

    :param tabs: A list of dictionaries representing each tab. Each dictionary should have:
                 - 'label': The text label of the tab.
                 - 'active': A boolean indicating if the tab is active.
                 - 'icon': (Optional) The FontAwesome icon name for the tab.
    :param _class: Additional CSS classes for the tabs container.
    """
    with div(_class=f"tabs {_class}", **kwargs) as tabs_div:
        with ul():
            for tab in tabs:
                with li(_class="is-active" if tab.get("active", False) else ""):
                    with a():
                        if "icon" in tab:
                            FontAwesomeIcon(tab["icon"], _class="is-small")
                        span(tab["label"])
    return tabs_div


__all__ = [
    'Tabs',
    'TabsAlignment',
    'TabsSize',
    'TabsStyle',
]
