# src\file_conversor\backend\gui\pdf\_dom_page.py

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


def pdf_index_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("PDF"),
        'url': url_for('pdf_index'),
        'active': active,
    }


def pdf_compress_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Compress"),
        'url': url_for('pdf_compress'),
        'active': active,
    }


def pdf_convert_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Convert"),
        'url': url_for('pdf_convert'),
        'active': active,
    }


def pdf_decrypt_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Decrypt"),
        'url': url_for('pdf_decrypt'),
        'active': active,
    }


def pdf_encrypt_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Encrypt"),
        'url': url_for('pdf_encrypt'),
        'active': active,
    }


def pdf_extract_img_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Extract Images"),
        'url': url_for('pdf_extract_img'),
        'active': active,
    }


def pdf_extract_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Extract Pages"),
        'url': url_for('pdf_extract'),
        'active': active,
    }


def pdf_merge_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Merge"),
        'url': url_for('pdf_merge'),
        'active': active,
    }


def pdf_ocr_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("OCR"),
        'url': url_for('pdf_ocr'),
        'active': active,
    }


def pdf_repair_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Repair"),
        'url': url_for('pdf_repair'),
        'active': active,
    }


def pdf_rotate_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Rotate"),
        'url': url_for('pdf_rotate'),
        'active': active,
    }


def pdf_split_nav_item(
    active: bool = False
) -> dict[str, Any]:
    return {
        'label': _("Split"),
        'url': url_for('pdf_split'),
        'active': active,
    }


__all__ = [
    'pdf_index_nav_item',
    'pdf_compress_nav_item',
    'pdf_convert_nav_item',
    'pdf_decrypt_nav_item',
    'pdf_encrypt_nav_item',
    'pdf_extract_img_nav_item',
    'pdf_extract_nav_item',
    'pdf_merge_nav_item',
    'pdf_ocr_nav_item',
    'pdf_repair_nav_item',
    'pdf_rotate_nav_item',
    'pdf_split_nav_item',
]
