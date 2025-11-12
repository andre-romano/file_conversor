# src/file_conversor/backend/gui/text/compress.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend import TextBackend

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


def PageTextCompress():
    return PageForm(
        InputFilesField(
            *TextBackend.SUPPORTED_IN_FORMATS,
            description=_("Text files"),
        ),
        OutputDirField(),
        api_endpoint=f"{url_for('api_text_compress')}",
        nav_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Text"),
                'url': url_for('text_index'),
            },
            {
                'label': _("Compress"),
                'url': url_for('text_compress'),
                'active': True,
            },
        ],
        _title=f"{_('Compress Text')} - File Conversor",
    )


def text_compress():
    return render_template_string(str(
        PageTextCompress()
    ))
