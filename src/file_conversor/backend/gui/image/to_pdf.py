# src/file_conversor/backend/gui/image/to_pdf.py

from pathlib import Path
from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.image import Img2PDFBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.image._dom_page import image_index_nav_item, image_to_pdf_nav_item

from file_conversor.utils.bulma_utils import InputFilesField, OutputFileField, ImageDPIField, ImageFitField, ImagePageSizeField, ImageSetMetadataField
from file_conversor.utils.dominate_bulma import PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageImageToPDF():
    return PageForm(
        InputFilesField(
            *[f for f in Img2PDFBackend.SUPPORTED_IN_FORMATS],
            description=_("Image files"),
        ),
        ImageDPIField(),
        ImageFitField(),
        ImagePageSizeField(),
        OutputFileField(
            *[
                (f, f'{f.upper()} {_("file")}')
                for f in Img2PDFBackend.SUPPORTED_OUT_FORMATS
            ],
            current_value="output.pdf",
        ),
        ImageSetMetadataField(),
        api_endpoint=f"{url_for('api_image_to_pdf')}",
        nav_items=[
            home_nav_item(),
            image_index_nav_item(),
            image_to_pdf_nav_item(active=True),
        ],
        _title=f"{_('Image To PDF')} - File Conversor",
    )


def image_to_pdf():
    return render_template_string(str(
        PageImageToPDF()
    ))
