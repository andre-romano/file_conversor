# src/file_conversor/backend/gui/config/_tab_image.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.image import Img2PDFBackend, PillowBackend

from file_conversor.utils.bulma_utils import *
from file_conversor.utils.dominate_bulma import *

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation, AVAILABLE_LANGUAGES

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def TabConfigImage() -> tuple | list:
    return (
        ImageQualityField(),
        ImageDPIField(),
        ImageFitField(),
        ImagePageSizeField(),
        ImageResampleAlgorithmField(),
    )


__all__ = ['TabConfigImage']
