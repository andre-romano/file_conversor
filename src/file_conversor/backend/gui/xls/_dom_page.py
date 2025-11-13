# src\file_conversor\backend\gui\xls\_dom_page.py

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


def xls_index_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Spreadsheet"),
        'url': url_for('xls_index'),
        'active': active,
    }


def xls_convert_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Convert"),
        'url': url_for('xls_convert'),
        'active': active,
    }


__all__ = [
    'xls_index_nav_item',
    'xls_convert_nav_item',
]
