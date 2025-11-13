# src\file_conversor\backend\gui\image\_dom_page.py

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


def image_index_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Image"),
        'url': url_for('image_index'),
        'active': active,
    }


def image_antialias_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Antialias"),
        'url': url_for('image_antialias'),
        'active': active,
    }


def image_blur_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Blur"),
        'url': url_for('image_blur'),
        'active': active,
    }


def image_compress_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Compress"),
        'url': url_for('image_compress'),
        'active': active,
    }


def image_convert_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Convert"),
        'url': url_for('image_convert'),
        'active': active,
    }


def image_enhance_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Enhance"),
        'url': url_for('image_enhance'),
        'active': active,
    }


def image_filter_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Filter"),
        'url': url_for('image_filter'),
        'active': active,
    }


def image_info_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Info"),
        'url': url_for('image_info'),
        'active': active,
    }


def image_mirror_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Mirror"),
        'url': url_for('image_mirror'),
        'active': active,
    }


def image_render_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Render"),
        'url': url_for('image_render'),
        'active': active,
    }


def image_resize_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Resize"),
        'url': url_for('image_resize'),
        'active': active,
    }


def image_rotate_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Rotate"),
        'url': url_for('image_rotate'),
        'active': active,
    }


def image_to_pdf_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("To PDF"),
        'url': url_for('image_to_pdf'),
        'active': active,
    }


def image_unsharp_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Unsharp"),
        'url': url_for('image_unsharp'),
        'active': active,
    }


__all__ = [
    'image_index_nav_item',
    'image_antialias_nav_item',
    'image_blur_nav_item',
    'image_compress_nav_item',
    'image_convert_nav_item',
    'image_enhance_nav_item',
    'image_filter_nav_item',
    'image_info_nav_item',
    'image_mirror_nav_item',
    'image_render_nav_item',
    'image_resize_nav_item',
    'image_rotate_nav_item',
    'image_to_pdf_nav_item',
    'image_unsharp_nav_item',
]
