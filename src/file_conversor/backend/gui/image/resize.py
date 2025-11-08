# src/file_conversor/backend/gui/image/resize.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.image import PillowBackend

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


def PageImageResize():
    return PageForm(
        InputFilesField(
            *[f for f in PillowBackend.SUPPORTED_IN_FORMATS],
            description=_("Image files"),
        ),
        ImageScaleField(),
        ImageResampleAlgorithmField(),
        OutputDirField(),
        api_endpoint=f"{url_for('api_image_resize')}",
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
                'label': _("Resize"),
                'url': url_for('image_resize'),
                'active': True,
            },
        ],
        _title=f"{_('Image Resize')} - File Conversor",
    )


def image_resize():
    return render_template_string(str(
        PageImageResize()
    ))
