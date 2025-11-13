# src\file_conversor\backend\gui\text\_dom_page.py

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


def text_index_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Text"),
        'url': url_for('text_index'),
        'active': active,
    }


def text_check_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Check"),
        'url': url_for('text_check'),
        'active': active,
    }


def text_compress_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Compress"),
        'url': url_for('text_compress'),
        'active': active,
    }


def text_convert_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Convert"),
        'url': url_for('text_convert'),
        'active': active,
    }


__all__ = [
    'text_index_nav_item',
    'text_check_nav_item',
    'text_compress_nav_item',
    'text_convert_nav_item',
]
