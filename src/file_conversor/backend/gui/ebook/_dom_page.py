# src\file_conversor\backend\gui\ebook\_dom_page.py

from flask import url_for
from typing import Any

# user-provided modules
from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def ebook_index_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Ebook"),
        'url': url_for('ebook_index'),
        'active': active,
    }


def ebook_convert_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Convert"),
        'url': url_for('ebook_convert'),
        'active': active,
    }


__all__ = [
    'ebook_index_nav_item',
    'ebook_convert_nav_item',
]
