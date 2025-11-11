# src/file_conversor/backend/gui/pdf/repair.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.pdf.pikepdf_backend import PikePDFBackend

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


def PagePDFRepair():
    return PageForm(
        InputFilesField(
            *PikePDFBackend.SUPPORTED_IN_FORMATS,
            description=_("PDF files"),
        ),
        PDFPasswordField(),
        OutputDirField(),
        api_endpoint=f"{url_for('api_pdf_repair')}",
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
                'label': _("Repair"),
                'url': url_for('pdf_repair'),
                'active': True,
            },
        ],
        _title=f"{_('Repair PDF')} - File Conversor",
    )


def pdf_repair():
    return render_template_string(str(
        PagePDFRepair()
    ))
