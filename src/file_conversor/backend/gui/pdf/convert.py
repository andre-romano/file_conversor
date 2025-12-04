# src/file_conversor/backend/gui/pdf/convert.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.pdf import PyMuPDFBackend, PDF2DOCXBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.pdf._dom_page import pdf_convert_nav_item, pdf_index_nav_item

from file_conversor.utils.bulma_utils import FileFormatField, InputFilesField, OutputDirField, ImageDPIField, PDFPasswordField
from file_conversor.utils.dominate_bulma import PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PagePDFConvert():
    return PageForm(
        InputFilesField(
            "pdf",
            description=_("PDF files"),
        ),
        FileFormatField(
            *[
                (f, f.upper())
                for f in {
                    **PDF2DOCXBackend.SUPPORTED_OUT_FORMATS,
                    **PyMuPDFBackend.SUPPORTED_OUT_FORMATS
                }
            ],
            current_value="docx",
        ),
        ImageDPIField(),
        PDFPasswordField(),
        OutputDirField(),
        api_endpoint=f"{url_for('api_pdf_convert')}",
        nav_items=[
            home_nav_item(),
            pdf_index_nav_item(),
            pdf_convert_nav_item(active=True),
        ],
        _title=f"{_('PDF Convert')} - File Conversor",
    )


def pdf_convert():
    return render_template_string(str(
        PagePDFConvert()
    ))
