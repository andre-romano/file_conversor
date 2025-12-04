# src/file_conversor/backend/gui/pdf/ocr.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.pdf import OcrMyPDFBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.pdf._dom_page import pdf_index_nav_item, pdf_ocr_nav_item

from file_conversor.utils.bulma_utils import InputFilesField, OutputDirField, PDFLanguageField
from file_conversor.utils.dominate_bulma import PageForm

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
            *OcrMyPDFBackend.SUPPORTED_IN_FORMATS,
            description=_("PDF files"),
        ),
        PDFLanguageField(),
        OutputDirField(),
        api_endpoint=f"{url_for('api_pdf_ocr')}",
        nav_items=[
            home_nav_item(),
            pdf_index_nav_item(),
            pdf_ocr_nav_item(active=True),
        ],
        _title=f"{_('OCR Pages')} - File Conversor",
    )


def pdf_ocr():
    return render_template_string(str(
        PagePDFOcr()
    ))
