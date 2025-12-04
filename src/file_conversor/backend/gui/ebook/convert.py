# src/file_conversor/backend/gui/ebook/convert.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.ebook import CalibreBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.ebook._dom_page import ebook_convert_nav_item, ebook_index_nav_item

from file_conversor.utils.bulma_utils import FileFormatField, InputFilesField, OutputDirField
from file_conversor.utils.dominate_bulma import PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageEbookConvert():
    return PageForm(
        InputFilesField(
            *[f for f in CalibreBackend.SUPPORTED_IN_FORMATS],
            description=_("Ebook files"),
        ),
        FileFormatField(*[
            (q, q.upper())
            for q in CalibreBackend.SUPPORTED_OUT_FORMATS
        ], current_value='pdf'),
        OutputDirField(),
        api_endpoint=f"{url_for('api_ebook_convert')}",
        nav_items=[
            home_nav_item(),
            ebook_index_nav_item(),
            ebook_convert_nav_item(active=True),
        ],
        _title=f"{_('Ebook Convert')} - File Conversor",
    )


def ebook_convert():
    return render_template_string(str(
        PageEbookConvert()
    ))
