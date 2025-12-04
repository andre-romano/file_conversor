# src/file_conversor/backend/gui/image/enhance.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.image import PillowBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.image._dom_page import image_enhance_nav_item, image_index_nav_item

from file_conversor.utils.bulma_utils import BrightnessField, ColorField, ContrastField, SharpnessField, InputFilesField, OutputDirField
from file_conversor.utils.dominate_bulma import PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageImageEnhance():
    return PageForm(
        InputFilesField(
            *[f for f in PillowBackend.SUPPORTED_IN_FORMATS],
            description=_("Image files"),
        ),
        BrightnessField(),
        ColorField(),
        ContrastField(),
        SharpnessField(),
        OutputDirField(),
        api_endpoint=f"{url_for('api_image_enhance')}",
        nav_items=[
            home_nav_item(),
            image_index_nav_item(),
            image_enhance_nav_item(active=True),
        ],
        _title=f"{_('Image Enhance')} - File Conversor",
    )


def image_enhance():
    return render_template_string(str(
        PageImageEnhance()
    ))
