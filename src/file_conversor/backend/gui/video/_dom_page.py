# src\file_conversor\backend\gui\video\_dom_page.py

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


def video_index_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Video"),
        'url': url_for('video_index'),
        'active': active,
    }


def video_check_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Check"),
        'url': url_for('video_check'),
        'active': active,
    }


def video_compress_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Compress"),
        'url': url_for('video_compress'),
        'active': active,
    }


def video_convert_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Convert"),
        'url': url_for('video_convert'),
        'active': active,
    }


def video_enhance_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Enhance"),
        'url': url_for('video_enhance'),
        'active': active,
    }


def video_info_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Info"),
        'url': url_for('video_info'),
        'active': active,
    }


def video_mirror_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Mirror"),
        'url': url_for('video_mirror'),
        'active': active,
    }


def video_resize_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Resize"),
        'url': url_for('video_resize'),
        'active': active,
    }


def video_rotate_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Rotate"),
        'url': url_for('video_rotate'),
        'active': active,
    }


__all__ = [
    'video_index_nav_item',
    'video_check_nav_item',
    'video_compress_nav_item',
    'video_convert_nav_item',
    'video_enhance_nav_item',
    'video_info_nav_item',
    'video_mirror_nav_item',
    'video_resize_nav_item',
    'video_rotate_nav_item',
]
