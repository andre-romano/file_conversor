# src/file_conversor/backend/gui/pdf/split.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.pdf._dom_page import pdf_index_nav_item, pdf_split_nav_item

from file_conversor.utils.bulma_utils import InputFilesField, OutputDirField, PDFPasswordField
from file_conversor.utils.dominate_bulma import PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PagePDFSplit():
    return PageForm(
        InputFilesField(
            *PyPDFBackend.SUPPORTED_IN_FORMATS,
            description=_("PDF files"),
        ),
        PDFPasswordField(),
        OutputDirField(),
        api_endpoint=f"{url_for('api_pdf_split')}",
        nav_items=[
            home_nav_item(),
            pdf_index_nav_item(),
            pdf_split_nav_item(active=True),
        ],
        _title=f"{_('Split PDF')} - File Conversor",
    )


def pdf_split():
    return render_template_string(str(
        PagePDFSplit()
    ))
