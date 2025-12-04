# src\file_conversor\backend\gui\_components\navbar.py

from typing import Any

from file_conversor.utils.dominate_utils import a, div, hr, img, nav, span


def NavbarDivider(_class: str = "", **kwargs):
    """
    Create a Navbar divider component.

    :param _class: Additional CSS classes to apply to the divider.
    """
    return hr(_class=f"navbar-divider {_class}", **kwargs)


def NavbarItem(*content, _href: str, _class: str = "", **kwargs):
    """
    Create a Navbar item component.

    :param content: The content to display inside the navbar item.
    :param _href: The URL the navbar item links to.
    :param _class: Additional CSS classes to apply to the navbar item.
    """
    with a(_class=f"navbar-item {_class}", _href=_href, **kwargs) as item:
        for c in content:
            if not c:
                continue
            item.add(c)
    return item


def NavbarDropdown(*items, label: str, _class: str = "", **kwargs):
    """
    Create a Navbar dropdown component.

    :param items: The items to include in the dropdown.
    :param label: The label for the dropdown toggle.    
    :param _class: Additional CSS classes to apply to the dropdown.
    """
    with div(_class=f"navbar-item has-dropdown {_class}", **kwargs) as dropdown:
        with a(_class="navbar-link"):
            dropdown.add(label)
        with div(_class="navbar-dropdown"):
            for item in items:
                if not item:
                    continue
                dropdown.add(item)
    return dropdown


def Navbar(
        title: Any = None,
        navbar_start: list[Any] | None = None,
        navbar_end: list[Any] | None = None,
        **kwargs
):
    """
    Create a Navbar component.

    :param title: The title or breadcrumb component to display in the navbar.
    :param navbar_start: Additional components to display on the left side of the navbar.
    :param navbar_end: Additional components to display on the right side of the navbar.
    """
    with nav(
        _class="navbar is-fixed-top is-light has-border has-shadow is-flex "
               "is-justify-content-space-between is-align-items-center",
        _role="navigation",
        _aria_label="main navigation",
        **{"x-data": "{ open: false }"},
        **kwargs,
    ) as component:

        # Navbar brand section (logo and burger)
        with div(_class="navbar-brand"):
            with a(_class="navbar-item", _href="/"):
                img(_height="140", _src="/icons/icon.png", _alt="")
                span("File Conversor", _class="is-size-6 has-text-weight-bold")

            # Mobile burger button
            with a(
                _role="button",
                _class="navbar-burger",
                _aria_label="menu",
                _aria_expanded="false",
                _data_target="navbarMenuContent",
                **{
                    "@click": "open = ! open",
                }
            ):
                span(_aria_hidden="true")
                span(_aria_hidden="true")
                span(_aria_hidden="true")
                span(_aria_hidden="true")

        # Navbar title + breadcrumbs
        with div(_class="navbar-title is-flex is-align-items-center") as title_container:
            if title:
                title_container.add(title)

        # Navbar menu (right-aligned)
        with div(
            _id="navbarMenuContent",
            **{":class": "open ? 'navbar-menu is-active' : 'navbar-menu'"}
        ):
            # Navbar start (left side)
            with div(_class="navbar-start") as navbar_start_container:
                navbar_start_container.add(*(navbar_start or []))

            # Navbar end (right side)
            with div(_class="navbar-end") as navbar_end_container:
                navbar_end_container.add(*(navbar_end or []))
    return component


__all__ = [
    "Navbar",
    "NavbarItem",
    "NavbarDropdown",
    "NavbarDivider",
]
