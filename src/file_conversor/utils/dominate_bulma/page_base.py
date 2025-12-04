# src\file_conversor\utils\dominate_bulma\page_base.py

import dominate
import dominate.tags

from typing import cast

# user-provided modules
from file_conversor.utils.dominate_bulma.modal import ModalCard
from file_conversor.utils.dominate_bulma.navbar import Navbar
from file_conversor.utils.dominate_bulma.footer import Footer
from file_conversor.utils.dominate_bulma.status_bar import StatusBar

from file_conversor.utils.dominate_utils import div, document, meta, script, link

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation, AVAILABLE_LANGUAGES

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


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
        with cast(dominate.tags.body, component.body) as body:
            body.set_attribute("style", f"zoom: {CONFIG['gui-zoom']}%;")

            body.set_attribute("x-data", f"""{{ }}""")
            body.set_attribute(":class", f"""{{
                'is-cursor-wait': $store.status_bar.started && ! $store.status_bar.finished,
            }}""")

            # modal
            ModalCard(
                _class_head="p-5",
                _class_body="p-5",
                _class_foot="p-4",
            )

            # navbar
            Navbar(title=nav_title)

            with div(_id="main-app", _class="container") as main_app:
                main_app.add(*content)

            # footer
            Footer()
            StatusBar()

            # scripts
            script(_src="/static/js/base.js", _type="module", _defer=True)

            # alpine
            script(_src="/static/js/libs/alpine.mask.min.js", _defer=True)
            script(_src="/static/js/libs/alpine.sort.min.js", _defer=True)
            script(_src="/static/js/libs/alpine.min.js", _defer=True)
    return component


__all__ = [
    'PageBase'
]
