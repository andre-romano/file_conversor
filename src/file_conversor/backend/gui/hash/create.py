# src/file_conversor/backend/gui/hash/create.py

from pathlib import Path
from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.hash_backend import HashBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.hash._dom_page import hash_create_nav_item, hash_index_nav_item

from file_conversor.utils.bulma_utils import InputFilesField, OutputFileField
from file_conversor.utils.dominate_bulma import PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageHashCreate():
    return PageForm(
        InputFilesField(),
        OutputFileField(
            *[
                (f, f'{f.upper()} {_("file")}')
                for f in HashBackend.SUPPORTED_OUT_FORMATS
            ],
            current_value="output.sha256",
        ),
        api_endpoint=f"{url_for('api_hash_create')}",
        nav_items=[
            home_nav_item(),
            hash_index_nav_item(),
            hash_create_nav_item(active=True),
        ],
        _title=f"{_('Hash Create')} - File Conversor",
    )


def hash_create():
    return render_template_string(str(
        PageHashCreate()
    ))


__all__ = [
    'hash_create',
]
