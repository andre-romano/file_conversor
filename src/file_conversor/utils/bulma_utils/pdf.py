# src\file_conversor\utils\bulma_utils\pdf.py

from typing import Any

# user-provided modules
from file_conversor.backend.pdf import GhostscriptBackend, PikePDFBackend, PyPDFBackend, OcrMyPDFBackend

from file_conversor.utils.dominate_bulma.form_field import FormFieldHorizontal
from file_conversor.utils.dominate_bulma.form_input import FormFieldInput
from file_conversor.utils.dominate_bulma.form_select import FormFieldSelect

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_language_name, get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def PDFCompressionField():
    """Create a form field for PDF compression selection."""
    return FormFieldHorizontal(
        FormFieldSelect(
            *[
                (k, k.upper())
                for k in GhostscriptBackend.Compression.get_dict()
            ],
            current_value=str(CONFIG["pdf-compression"]),
            _name="pdf-compression",
            help=_("Select the PDF compression level to apply. Higher compression may reduce quality."),
        ),
        label_text=_("PDF Compression"),
    )


def PDFPasswordField(
    _validation_expr: str = "value.length >= 0",
    _name: str = "password",
    _placeholder=_('Enter password (optional)'),
    help: str = _("Password used to encrypt/decrypt the PDF files."),
    label_text: str = _("Password"),
    **kwargs: Any,
):
    """Create a form field for PDF password input."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr=_validation_expr,
            _type="password",
            _name=_name,
            _placeholder=_placeholder,
            help=help,
            **kwargs,
        ),
        label_text=label_text,
    )


def PDFEncryptionAlgorithmField():
    """Create a form field for PDF encryption algorithm selection."""
    return FormFieldHorizontal(
        FormFieldSelect(
            *[
                (k, k.upper())
                for k in PyPDFBackend.EncryptionAlgorithm.get_dict()
            ],
            current_value="AES-256",
            _name="pdf-encryption-algorithm",
            help=_("Select the PDF encryption algorithm to use. Stronger algorithms (e.g., AES-256) provide better security."),
        ),
        label_text=_("PDF Encryption Algorithm"),
    )


def PDFPagesField(
        _validation_expr: str = "value.length > 0",
        _name: str = "pages",
        help: str = _("PDF pages to extract (comma-separated list). Format 'start-end'."),
        label_text: str = _("Pages"),
        **kwargs: Any,
):
    """Create a form field for specifying PDF pages to extract."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr=_validation_expr,
            _type="text",
            _name=_name,
            help=help,
            **kwargs,
        ),
        label_text=label_text,
    )


def PDFLanguageField():
    """Create a form field for specifying OCR languages."""
    backend = OcrMyPDFBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE['verbose'],
    )
    languages = [
        (k, get_language_name(k))
        for k in backend.get_available_languages().union(backend.get_available_remote_languages())
    ]
    languages.sort(key=lambda x: x[1])  # sort by language name
    return FormFieldHorizontal(
        FormFieldSelect(
            *languages,
            current_value="eng",
            _name="pdf-language",
            help=_("Select the OCR language to use."),
        ),
        label_text=_("OCR Language"),
    )


__all__ = [
    "PDFCompressionField",
    "PDFPasswordField",
    "PDFEncryptionAlgorithmField",
    "PDFPagesField",
    "PDFLanguageField",
]
