# src\file_conversor\utils\dominate_bulma\page_base.py

import dominate

from typing import cast

import dominate.tags

from file_conversor.utils.dominate_bulma.navbar import Navbar
from file_conversor.utils.dominate_bulma.footer import Footer
from file_conversor.utils.dominate_bulma.status_bar import StatusBar

from file_conversor.utils.dominate_utils import *


def PageBase(
        *content,
        nav_title,
        _title: str,
        **kwargs
):
    """
    Create the base page structure.

    :param _title: The title of the page.
    :param nav_title: The title or breadcrumb component for the navbar.
    :param content: The main content of the page.
    """
    with document(
        title=_title,
        _lang="en",
        _class="has-navbar-fixed-top has-status-bar-fixed-bottom",
        **kwargs,
    ) as component:
        with cast(dominate.tags.head, component.head):
            meta(_charset="UTF-8")
            meta(_name="viewport", _content="width=device-width, initial-scale=1.0")
            # title(_title)

            # Favicon
            link(_rel="icon", _type="image/x-icon", _href="/icons/icon.png")
            link(_rel="icon", _type="image/png", _href="/icons/icon.png")

            # Libraries CSS
            link(_rel="stylesheet", _href="/static/css/bulma.min.css")
            link(_rel="stylesheet", _href="/static/css/font-awesome.all.min.css")

            # Custom CSS
            link(_rel="stylesheet", _href="/static/css/base.css")
        with cast(dominate.tags.body, component.body):
            # navbar
            Navbar(title=nav_title)

            with div(_id="main-app", _class="container") as main_app:
                main_app.add(*content)

            # footer
            Footer()
            StatusBar()

            # scripts
            script(_src="/static/js/base.js", _defer=True)

            # alpine
            script(_src="/static/js/alpine.mask.min.js", _defer=True)
            script(_src="/static/js/alpine.sort.min.js", _defer=True)
            script(_src="/static/js/alpine.min.js", _defer=True)
    return component


__all__ = [
    'PageBase'
]
