# src\file_conversor\utils\bulma_utils\image.py

from typing import Any

# user-provided modules
from file_conversor.backend.audio_video.ffmpeg_backend import FFmpegBackend

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


__all__ = [
    "ImageQualityField",
]
