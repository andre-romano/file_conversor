# src/file_conversor/backend/gui/ebook/convert.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.ebook import CalibreBackend

from file_conversor.utils.bulma_utils import *
from file_conversor.utils.dominate_bulma import *

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
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Ebook"),
                'url': url_for('ebook_index'),
            },
            {
                'label': _("Convert"),
                'url': url_for('ebook_convert'),
                'active': True,
            },
        ],
        _title=f"{_('Ebook Convert')} - File Conversor",
    )


def ebook_convert():
    return render_template_string(str(
        PageEbookConvert()
    ))
