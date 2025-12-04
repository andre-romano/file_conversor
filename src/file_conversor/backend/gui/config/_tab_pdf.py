# src/file_conversor/backend/gui/config/_tab_pdf.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.utils.bulma_utils import PDFCompressionField

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
        PDFCompressionField(),
    )


__all__ = ['TabConfigPDF']
