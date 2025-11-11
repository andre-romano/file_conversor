# src/file_conversor/backend/gui/pdf/extract.py

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


def PagePDFExtract():
    return PageForm(
        InputFilesField(
            *PyPDFBackend.SUPPORTED_IN_FORMATS,
            description=_("PDF files"),
        ),
        PDFPagesField(
            _name="pages",
            help=_("Pages to extract from the PDF. Use commas to separate pages and hyphens for ranges (e.g., 1,3-5)."),
            label_text=_("Pages"),
        ),
        PDFPasswordField(
            _validation_expr="value.length >= 0",
            _name="password",
            _placeholder=_('Enter password (optional)'),
            help=_("Password to decrypt protected PDF files."),
            label_text=_("Password"),
        ),
        OutputDirField(),
        api_endpoint=f"{url_for('api_pdf_extract')}",
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
                'label': _("Extract Pages"),
                'url': url_for('pdf_extract'),
                'active': True,
            },
        ],
        _title=f"{_('Extract Pages')} - File Conversor",
    )


def pdf_extract():
    return render_template_string(str(
        PagePDFExtract()
    ))
