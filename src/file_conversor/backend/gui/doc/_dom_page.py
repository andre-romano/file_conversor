# src\file_conversor\backend\gui\doc\_dom_page.py

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


def doc_index_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Document"),
        'url': url_for('doc_index'),
        'active': active,
    }


def doc_convert_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Convert"),
        'url': url_for('doc_convert'),
        'active': active,
    }


__all__ = [
    'doc_index_nav_item',
    'doc_convert_nav_item',
]
