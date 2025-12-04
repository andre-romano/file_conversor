# src/file_conversor/backend/gui/xls/convert.py

from typing import Any
from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.office import LibreofficeCalcBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.xls._dom_page import xls_convert_nav_item, xls_index_nav_item

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


def PageConvert():
    return PageForm(
        InputFilesField(
            *[f for f in LibreofficeCalcBackend.SUPPORTED_IN_FORMATS],
            description=_("Spreadsheet files"),
        ),
        FileFormatField(*[
            (f, f.upper())
            for f in LibreofficeCalcBackend.SUPPORTED_OUT_FORMATS
        ], current_value="pdf"),
        OutputDirField(),
        api_endpoint=f"{url_for('api_xls_convert')}",
        nav_items=[
            home_nav_item(),
            xls_index_nav_item(),
            xls_convert_nav_item(active=True),
        ],
        _title=_("Convert XLS - File Conversor"),
    )


def xls_convert():
    return render_template_string(str(
        PageConvert()
    ))
