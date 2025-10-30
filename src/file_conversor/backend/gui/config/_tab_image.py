# src/file_conversor/backend/gui/config/_tab_image.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.image import Img2PDFBackend, PillowBackend

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
        FormFieldHorizontal(
            FormFieldInput(
                validation_expr="Number.parseInt(value) >= 1 && Number.parseInt(value) <= 100",
                current_value=CONFIG['image-quality'],
                _name="image-quality",
                _type="number",
                help=_("Set the default quality for image conversions (1-100). Higher values mean better quality and larger file size."),
            ),
            label_text=_("Image Quality (%)"),
        ),
        FormFieldHorizontal(
            FormFieldInput(
                validation_expr="Number.parseInt(value) >= 40 && Number.parseInt(value) <= 3600",
                current_value=CONFIG['image-dpi'],
                _name="image-dpi",
                _type="number",
                help=_("Set the default DPI (dots per inch) for image conversions (40-3600). Higher values mean better quality and larger file size."),
            ),
            label_text=_("Image DPI (dpi)"),
        ),
        FormFieldHorizontal(
            FormFieldSelect(
                *[
                    (f, f.upper())
                    for f in Img2PDFBackend.FIT_MODES
                ],
                current_value=CONFIG['image-fit'],
                _name="image-fit",
                help=_("Fit mode for images converted to PDF. 'into' fits the image within the page, 'fill' fills the entire page."),
            ),
            label_text=_("Image Fit Mode"),
        ),
        FormFieldHorizontal(
            FormFieldSelect(
                *[
                    (f, f.upper())
                    for f in ['null', *Img2PDFBackend.PAGE_LAYOUT.keys()]
                ],
                current_value=CONFIG['image-page-size'],
                _name="image-page-size",
                help=_("Page size for images converted to PDF. Choose from standard sizes or 'None' for original size."),
            ),
            label_text=_("Image Page Size"),
        ),
        FormFieldHorizontal(
            FormFieldSelect(
                *[
                    (f, f.upper())
                    for f in PillowBackend.RESAMPLING_OPTIONS
                ],
                current_value=CONFIG['image-resampling'],
                _name="image-resampling",
                help=_("Resampling method for images converted to PDF. Choose from standard methods or 'None' for original size."),
            ),
            label_text=_("Image Resampling"),
        ),
    )


__all__ = ['TabConfigImage']
