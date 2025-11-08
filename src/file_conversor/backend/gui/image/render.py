# src/file_conversor/backend/gui/image/render.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.image import PyMuSVGBackend

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
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Image"),
                'url': url_for('image_index'),
            },
            {
                'label': _("Render"),
                'url': url_for('image_render'),
                'active': True,
            },
        ],
        _title=f"{_('Image Render')} - File Conversor",
    )


def image_render():
    return render_template_string(str(
        PageImageRender()
    ))
