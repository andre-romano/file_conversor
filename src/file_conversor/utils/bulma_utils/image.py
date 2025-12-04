# src\file_conversor\utils\bulma_utils\image.py

from typing import Any

# user-provided modules
from file_conversor.backend.image import PillowBackend, Img2PDFBackend

from file_conversor.utils.dominate_bulma.form_checkbox import FormFieldCheckbox
from file_conversor.utils.dominate_bulma.form_field import FormFieldHorizontal
from file_conversor.utils.dominate_bulma.form_input import FormFieldInput
from file_conversor.utils.dominate_bulma.form_select import FormFieldSelect

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


def ImageRotationField():
    """Create a form field for image rotation."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) >= -360 && Number.parseInt(value) <= 360",
            current_value='0',
            _name="image-rotation",
            _type="number",
            step="90",
            help=_("Rotation in degrees. Valid values are between -360 (anti-clockwise) and 360 (clockwise) rotation."),
        ),
        label_text=_("Rotation (deg)"),
    )


def ImageScaleField():
    """Create a form field for image scale adjustment."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseFloat(value) > 0",
            current_value='1.0',
            _name="image-scale",
            _type="number",
            step="0.1",
            help=_("Scale factor for resizing the image. Must be a positive number."),
        ),
        label_text=_("Scale Factor"),
    )


def ImageResampleAlgorithmField():
    """Create a form field for selecting resample algorithm."""
    return FormFieldHorizontal(
        FormFieldSelect(
            *[
                (k, k.upper())
                for k in PillowBackend.RESAMPLING_OPTIONS
            ],
            current_value=CONFIG["image-resampling"],
            _name="image-resampling",
            help=_("Select the resampling algorithm to use when resizing images."),
        ),
        label_text=_("Resampling Algorithm"),
    )


def ImageFitField():
    """Create a form field for image fit option."""
    return FormFieldHorizontal(
        FormFieldSelect(
            *[
                (k, k.upper())
                for k in Img2PDFBackend().FIT_MODES
            ],
            current_value=CONFIG["image-fit"],
            _name="image-fit",
            help=_("Select how to fit the image into the page when converting to PDF. Valid only if page size is defined."),
        ),
        label_text=_("Image Fit"),
    )


def ImagePageSizeField():
    """Create a form field for image page size option."""
    return FormFieldHorizontal(
        FormFieldSelect(
            ('null', _('Not defined')),
            *[
                (k, k.upper())
                for k in Img2PDFBackend().PAGE_LAYOUT
            ],
            current_value=CONFIG["image-page-size"],
            _name="image-page-size",
            help=_("Select the page size for the output PDF. If not defined, PDF size will match image size."),
        ),
        label_text=_("Page Size"),
    )


def ImageSetMetadataField():
    """Create a form field for setting image metadata option."""
    return FormFieldCheckbox(
        current_value="off",
        _name="image-set-metadata",
        help=_("Include image metadata (EXIF, IPTC, etc) in the output file."),
        label_text=_("Set Metadata"),
    )


def ImageUnsharpStrengthField():
    """Create a form field for image unsharp strength adjustment."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) >= 1",
            current_value='130',
            _name="image-unsharp-strength",
            _type="number",
            step="10",
            help=_("Unsharp strength, in percent. Must be a positive integer."),
        ),
        label_text=_("Strength (%)"),
    )


def ImageUnsharpThresholdField():
    """Create a form field for image unsharp threshold adjustment."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) >= 1",
            current_value='4',
            _name="image-unsharp-threshold",
            _type="number",
            step="1",
            help=_("Threshold controls the minimum brightness change that will be sharpened. Must be a positive integer."),
        ),
        label_text=_("Threshold"),
    )


__all__ = [
    "ImageQualityField",
    "ImageRadiusField",
    "ImageAntialiasAlgorithmField",
    "ImageFilterField",
    "ImageDPIField",
    "ImageRotationField",
    "ImageScaleField",
    "ImageResampleAlgorithmField",
    "ImageFitField",
    "ImagePageSizeField",
    "ImageSetMetadataField",
    "ImageUnsharpStrengthField",
    "ImageUnsharpThresholdField",
]
