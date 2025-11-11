# src/file_conversor/backend/gui/pdf/decrypt.py

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


def PagePDFDecrypt():
    return PageForm(
        InputFilesField(
            *PyPDFBackend.SUPPORTED_IN_FORMATS,
            description=_("PDF files"),
        ),
        PasswordField(
            _name="password",
            help=_("Password used to decrypt the PDF files."),
            label_text=_("Password"),
        ),
        OutputDirField(),
        api_endpoint=f"{url_for('api_pdf_decrypt')}",
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
                'label': _("Decrypt"),
                'url': url_for('pdf_decrypt'),
                'active': True,
            },
        ],
        _title=f"{_('PDF Decrypt')} - File Conversor",
    )


def pdf_decrypt():
    return render_template_string(str(
        PagePDFDecrypt()
    ))
