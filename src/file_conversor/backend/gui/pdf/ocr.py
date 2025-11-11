# src/file_conversor/backend/gui/pdf/ocr.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.pdf import PyPDFBackend

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


def PagePDFOcr():
    return PageForm(
        InputFilesField(
            *PyPDFBackend.SUPPORTED_IN_FORMATS,
            description=_("PDF files"),
        ),
        PDFLanguageField(),
        OutputDirField(),
        api_endpoint=f"{url_for('api_pdf_ocr')}",
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
                'label': _("OCR Pages"),
                'url': url_for('pdf_ocr'),
                'active': True,
            },
        ],
        _title=f"{_('OCR Pages')} - File Conversor",
    )


def pdf_ocr():
    return render_template_string(str(
        PagePDFOcr()
    ))
