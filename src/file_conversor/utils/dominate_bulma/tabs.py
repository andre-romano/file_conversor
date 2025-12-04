# src\file_conversor\utils\bulma\tabs.py

from typing import Any

from file_conversor.utils.dominate_bulma.font_awesome_icon import FontAwesomeIcon
from file_conversor.utils.dominate_utils import a, div, li, span, ul


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
    active_tab: str = "",
    _class: str = "",
    _class_headers: str = "",
    _class_content: str = "",
    **kwargs,
):
    """
    Create a Bulma tabs component.

    :param tabs: A list of dictionaries representing each tab. Each dictionary should have:
                 - 'label': The text label of the tab.
                 - 'icon': (Optional) The FontAwesome icon name for the tab.
                 - 'content': The list of content to display when the tab is active.
    :param active_tab: The label of the tab that should be active by default.                 
    :param _class: Additional CSS classes for the tabs container.
    :param _class_headers: Additional CSS classes for the tab headers.
    :param _class_content: Additional CSS classes for the tab content area.
    """
    if not tabs:
        raise ValueError("At least one tab must be provided.")

    active_tab = active_tab or tabs[0]['label']
    if all(tab['label'] != active_tab for tab in tabs):
        raise ValueError("The active_tab must match one of the provided tab labels.")

    with div(_class=f"tabs {_class}", **{
        "x-data": f"""{{
            activeTab: '{active_tab}',
        }}""",
    }, **kwargs) as tabs_div:
        with ul(_class=f"tab-headers {_class_headers}"):
            for tab in tabs:
                with li(**{
                    ":class": f"""{{
                        'is-active': activeTab === '{tab['label']}'
                    }}"""
                }):
                    with a(**{
                        "@click.prevent": f"activeTab = '{tab['label']}'",
                    }):
                        if "icon" in tab:
                            FontAwesomeIcon(tab["icon"], _class="is-small")
                        span(tab["label"])
        for tab in tabs:
            with div(_class=f"tab-content {_class_content}", **{
                ":class": f"""{{
                    'is-hidden': activeTab !== '{tab['label']}'
                }}"""
            }) as tab_content_div:
                tab_content_div.add(*tab['content'])
    return tabs_div


__all__ = [
    'Tabs',
    'TabsAlignment',
    'TabsSize',
    'TabsStyle',
]
