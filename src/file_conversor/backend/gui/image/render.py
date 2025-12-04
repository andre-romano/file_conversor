# src/file_conversor/backend/gui/image/render.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.image import PyMuSVGBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.image._dom_page import image_index_nav_item, image_render_nav_item

from file_conversor.utils.bulma_utils import FileFormatField, InputFilesField, OutputDirField, ImageDPIField
from file_conversor.utils.dominate_bulma import PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageImageRender():
    return PageForm(
        InputFilesField(
            *[f for f in PyMuSVGBackend.SUPPORTED_IN_FORMATS],
            description=_("Image files"),
        ),
        FileFormatField(
            *[
                (f, f.upper())
                for f in PyMuSVGBackend.SUPPORTED_OUT_FORMATS
            ],
        ),
        ImageDPIField(),
        OutputDirField(),
        api_endpoint=f"{url_for('api_image_render')}",
        nav_items=[
            home_nav_item(),
            image_index_nav_item(),
            image_render_nav_item(active=True),
        ],
        _title=f"{_('Image Render')} - File Conversor",
    )


def image_render():
    return render_template_string(str(
        PageImageRender()
    ))
