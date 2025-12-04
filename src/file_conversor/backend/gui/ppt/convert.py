# src/file_conversor/backend/gui/ppt/convert.py

from flask import render_template, render_template_string, url_for
from typing import Any

# user-provided modules
from file_conversor.backend.office import LibreofficeImpressBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.ppt._dom_page import ppt_convert_nav_item, ppt_index_nav_item

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
            *[f for f in LibreofficeImpressBackend.SUPPORTED_IN_FORMATS],
            description=_("Presentation files")
        ),
        FileFormatField(
            *[
                (f, f.upper())
                for f in LibreofficeImpressBackend.SUPPORTED_OUT_FORMATS
            ],
            current_value="pdf",
        ),
        OutputDirField(),
        api_endpoint=f"{url_for('api_ppt_convert')}",
        nav_items=[
            home_nav_item(),
            ppt_index_nav_item(),
            ppt_convert_nav_item(active=True),
        ],
        _title=_("Convert PPT - File Conversor"),
    )


def ppt_convert():
    return render_template_string(str(
        PageConvert()
    ))
