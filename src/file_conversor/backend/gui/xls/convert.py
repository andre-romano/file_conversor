# src/file_conversor/backend/gui/xls/convert.py

from typing import Any
from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.office import XLS_BACKEND

from file_conversor.utils.bulma_utils import *
from file_conversor.utils.dominate_bulma import *
from file_conversor.utils.formatters import format_file_types_webview

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
            *[f for f in XLS_BACKEND.SUPPORTED_IN_FORMATS],
            description=_("Spreadsheet files"),
        ),
        FileFormatField(*[
            (f, f.upper())
            for f in XLS_BACKEND.SUPPORTED_OUT_FORMATS
        ], current_value="pdf"),
        OutputDirField(),
        OverwriteFilesField(),
        api_endpoint=f"{url_for('api_xls_convert')}",
        nav_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Spreadsheet Tools"),
                'url': url_for('xls_index'),
            },
            {
                'label': _("Convert"),
                'url': url_for('xls_convert'),
                'active': True,
            },
        ],
        _title=_("Convert XLS - File Conversor"),
    )


def xls_convert():
    return render_template_string(str(
        PageConvert()
    ))
