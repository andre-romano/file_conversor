# src\file_conversor\utils\bulma_utils\image.py

from typing import Any

# user-provided modules
from file_conversor.backend.image import PillowBackend

from file_conversor.utils.dominate_utils import *
from file_conversor.utils.dominate_bulma import *

from file_conversor.utils.formatters import format_file_types_webview

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def ImageQualityField():
    """Create a form field for image quality adjustment."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) >= 0 && Number.parseInt(value) <= 100",
            current_value=CONFIG["image-quality"],
            _name="image-quality",
            _type="number",
            step="10",
            help=_("Adjust image quality level. Value between 0 (lowest) to 100 (highest)."),
        ),
        label_text=_("Image Quality (%)"),
    )


def ImageRadiusField():
    """Create a form field for image radius adjustment."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) >= 1",
            current_value='3',
            _name="radius",
            _type="number",
            step="1",
            help=_("Box radius (in pixels). Must be a positive integer."),
        ),
        label_text=_("Box Radius (px)"),
    )


def ImageAntialiasAlgorithmField():
    """Create a form field for selecting antialias algorithm."""
    return FormFieldHorizontal(
        FormFieldSelect(
            *[
                (k, k.upper())
                for k in PillowBackend.AntialiasAlgorithm.get_dict()
            ],
            current_value='median',
            _name="algorithm",
            help=_("Select the antialias algorithm to use."),
        ),
        label_text=_("Algorithm"),
    )


def ImageFilterField():
    """Create a form field for image filter options."""
    return FormFieldHorizontal(
        FormFieldSelect(
            *[
                (k, k.upper())
                for k in PillowBackend.PILLOW_FILTERS
            ],
            _name="filter",
            help=_("Select the filter to apply to the image."),
        ),
        label_text=_("Filter"),
    )


def ImageDPIField():
    """Create a form field for DPI selection."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) > 0",
            current_value=str(CONFIG["image-dpi"]),
            _name="image-dpi",
            _type="number",
            step="100",
            help=_("Dots per inch (DPI) for rendering the image. Must be a positive integer."),
        ),
        label_text=_("DPI"),
    )


__all__ = [
    "ImageQualityField",
    "ImageRadiusField",
    "ImageAntialiasAlgorithmField",
    "ImageFilterField",
    "ImageDPIField",
]
