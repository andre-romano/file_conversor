# src/file_conversor/backend/gui/pdf/compress.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.pdf import GhostscriptBackend

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


def PagePDFCompress():
    return PageForm(
        InputFilesField(
            *GhostscriptBackend.SUPPORTED_IN_FORMATS,
            description=_("PDF files"),
        ),
        PDFCompressionField(),
        OutputDirField(),
        api_endpoint=f"{url_for('api_pdf_compress')}",
        nav_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("PDF"),
                'url': url_for('pdf_index'),
            },
            {
                'label': _("Compress"),
                'url': url_for('pdf_compress'),
                'active': True,
            },
        ],
        _title=f"{_('PDF Compress')} - File Conversor",
    )


def pdf_compress():
    return render_template_string(str(
        PagePDFCompress()
    ))
