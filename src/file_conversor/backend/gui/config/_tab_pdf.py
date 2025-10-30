# src/file_conversor/backend/gui/config/_tab_pdf.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.pdf.ghostscript_backend import GhostscriptBackend
from file_conversor.utils.dominate_bulma import *

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation, AVAILABLE_LANGUAGES

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def TabConfigPDF() -> tuple | list:
    return (
        FormFieldHorizontal(
            FormFieldSelect(
                *[
                    (f, f.upper())
                    for f in GhostscriptBackend.Compression.get_dict()
                ],
                current_value=CONFIG['pdf-compression'],
                _name="pdf-compression",
                help=_("Set the default PDF compression level. Higher compression results in lower quality."),
            ),
            label_text=_("PDF Compression"),
        ),
    )


__all__ = ['TabConfigPDF']
