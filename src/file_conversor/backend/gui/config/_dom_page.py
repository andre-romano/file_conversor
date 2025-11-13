# src\file_conversor\backend\gui\audio\_dom_page.py

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


def config_index_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Configuration"),
        'url': url_for('config_index'),
        'active': active,
    }


__all__ = [
    'config_index_nav_item',
]
