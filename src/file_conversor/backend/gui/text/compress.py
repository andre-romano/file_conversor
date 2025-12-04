# src/file_conversor/backend/gui/text/compress.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend import TextBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.text._dom_page import text_compress_nav_item, text_index_nav_item

from file_conversor.utils.bulma_utils import InputFilesField, OutputDirField
from file_conversor.utils.dominate_bulma import PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageTextCompress():
    return PageForm(
        InputFilesField(
            *TextBackend.SUPPORTED_IN_FORMATS,
            description=_("Text files"),
        ),
        OutputDirField(),
        api_endpoint=f"{url_for('api_text_compress')}",
        nav_items=[
            home_nav_item(),
            text_index_nav_item(),
            text_compress_nav_item(active=True),
        ],
        _title=f"{_('Compress Text')} - File Conversor",
    )


def text_compress():
    return render_template_string(str(
        PageTextCompress()
    ))
