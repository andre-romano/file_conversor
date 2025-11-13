# src\file_conversor\backend\gui\hash\_dom_page.py

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


def hash_index_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Hash"),
        'url': url_for('hash_index'),
        'active': active,
    }


def hash_check_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Check"),
        'url': url_for('hash_check'),
        'active': active,
    }


def hash_create_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Create"),
        'url': url_for('hash_create'),
        'active': active,
    }


__all__ = [
    'hash_index_nav_item',
    'hash_check_nav_item',
    'hash_create_nav_item',
]
