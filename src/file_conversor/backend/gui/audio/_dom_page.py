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


def audio_index_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Audio"),
        'url': url_for('audio_index'),
        'active': active,
    }


def audio_check_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Check"),
        'url': url_for('audio_check'),
        'active': active,
    }


def audio_convert_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Convert"),
        'url': url_for('audio_convert'),
        'active': active,
    }


def audio_info_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Info"),
        'url': url_for('audio_info'),
        'active': active,
    }


__all__ = [
    "audio_index_nav_item",
    "audio_check_nav_item",
    "audio_convert_nav_item",
    "audio_info_nav_item",
]
