# src/file_conversor/backend/gui/image/compress.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.image import CompressBackend

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


def PageImageCompress():
    return PageForm(
        InputFilesField(
            *[f for f in CompressBackend.SUPPORTED_IN_FORMATS],
            description=_("Image files"),
        ),
        ImageQualityField(),
        OutputDirField(),
        api_endpoint=f"{url_for('api_image_compress')}",
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
                'label': _("Compress"),
                'url': url_for('image_compress'),
                'active': True,
            },
        ],
        _title=f"{_('Image Compress')} - File Conversor",
    )


def image_compress():
    return render_template_string(str(
        PageImageCompress()
    ))
