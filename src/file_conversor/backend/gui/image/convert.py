# src/file_conversor/backend/gui/image/convert.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.image import PillowBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.image._dom_page import image_convert_nav_item, image_index_nav_item

from file_conversor.utils.bulma_utils import FileFormatField, InputFilesField, OutputDirField, ImageQualityField
from file_conversor.utils.dominate_bulma import PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageImageConvert():
    return PageForm(
        InputFilesField(
            *[f for f in PillowBackend.SUPPORTED_IN_FORMATS],
            description=_("Image files"),
        ),
        FileFormatField(*[
            (q, q.upper())
            for q in PillowBackend.SUPPORTED_OUT_FORMATS
        ], current_value='jpg'),
        ImageQualityField(),
        OutputDirField(),
        api_endpoint=f"{url_for('api_image_convert')}",
        nav_items=[
            home_nav_item(),
            image_index_nav_item(),
            image_convert_nav_item(active=True),
        ],
        _title=f"{_('Image Convert')} - File Conversor",
    )


def image_convert():
    return render_template_string(str(
        PageImageConvert()
    ))
