# src\file_conversor\utils\bulma_utils\pdf.py

from typing import Any

# user-provided modules
from file_conversor.backend.pdf import GhostscriptBackend, PikePDFBackend

from file_conversor.utils.dominate_utils import *
from file_conversor.utils.dominate_bulma import *

from file_conversor.utils.formatters import format_file_types_webview

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

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


__all__ = [
    "PDFCompressionField",
]
