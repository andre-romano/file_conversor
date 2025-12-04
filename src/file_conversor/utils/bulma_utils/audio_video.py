# src\file_conversor\utils\bulma_utils\audio_video.py

from typing import Any

# user-provided modules
from file_conversor.backend.audio_video.ffmpeg_backend import FFmpegBackend

from file_conversor.utils.dominate_bulma.form_field import FormFieldHorizontal
from file_conversor.utils.dominate_bulma.form_input import FormFieldInput
from file_conversor.utils.dominate_bulma.form_select import FormFieldSelect
from file_conversor.utils.dominate_bulma.form_checkbox import FormFieldCheckbox

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def TargetSizeField():
    """Create a form field for target file size input."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) >= 0",
            current_value="0",
            _name="target-size",
            _type="number",
            help=_("Set target file size (in MB) for the output video. Type 0 to skip size targeting (use encoding speed and quality options to find file size)."),
        ),
        label_text=_("Target Size (MB)"),
    )


def AudioBitrateField():
    """Create a form field for audio bitrate input."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) >= 0",
            current_value=CONFIG['audio-bitrate'],
            _name="audio-bitrate",
            _type="number",
            help=_("Set audio bitrate (in kbps). Type 0 to keep original audio bitrate."),
        ),
        label_text=_("Audio Bitrate (kbps)"),
    )


def VideoBitrateField():
    """Create a form field for video bitrate input."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) >= 0",
            current_value=CONFIG['video-bitrate'],
            _name="video-bitrate",
            _type="number",
            help=_("Set video bitrate (in kbps). Type 0 to keep original video bitrate."),
        ),
        label_text=_("Video Bitrate (kbps)"),
    )


def AudioCodecField():
    """Create a form field for audio codec selection."""
    return FormFieldHorizontal(
        FormFieldSelect(
            ('', _('Default')),
            *[
                (codec, codec.upper())
                for codec in FFmpegBackend.get_supported_audio_codecs()
            ],
            current_value="",
            _name="audio-codec",
            help=_("Select the audio codec to use for encoding. Not all codecs are supported for all formats."),
        ),
        label_text=_("Audio Codec"),
    )


def VideoCodecField():
    """Create a form field for video codec selection."""
    return FormFieldHorizontal(
        FormFieldSelect(
            ('', _('Default')),
            *[
                (codec, codec.upper())
                for codec in FFmpegBackend.get_supported_video_codecs()
            ],
            current_value="",
            _name="video-codec",
            help=_("Select the video codec to use for encoding. Not all codecs are supported for all formats."),
        ),
        label_text=_("Video Codec"),
    )


def VideoEncodingSpeedField():
    """Create a form field for video encoding speed selection."""
    return FormFieldHorizontal(
        FormFieldSelect(
            *[
                (speed, speed.upper())
                for speed in FFmpegBackend.ENCODING_SPEEDS
            ],
            current_value=CONFIG['video-encoding-speed'],
            _name="video-encoding-speed",
            help=_("Select the video encoding speed. Faster speeds result in lower quality and larger file sizes."),
        ),
        label_text=_("Video Encoding Speed"),
    )


def VideoQualityField():
    """Create a form field for video quality selection."""
    return FormFieldHorizontal(
        FormFieldSelect(
            *[
                (quality, quality.upper())
                for quality in FFmpegBackend.QUALITY_PRESETS
            ],
            current_value=CONFIG['video-quality'],
            _name="video-quality",
            help=_("Select the video quality preset. Higher quality results in larger file sizes."),
        ),
        label_text=_("Video Quality"),
    )


def ResolutionField():
    """Create a form field for video resolution input."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="/^\\d+:\\d+$/.test(value) || value === ''",
            current_value="",
            _name="resolution",
            _type="text",
            help=_("Set video resolution (e.g., 1920:1080). Leave empty to keep original resolution."),
        ),
        label_text=_("Resolution"),
    )


def FPSField():
    """Create a form field for frames per second (FPS) input."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) > 0 || value === ''",
            current_value="",
            _name="fps",
            _type="number",
            help=_("Set frames per second (FPS). Leave empty to keep original FPS."),
        ),
        label_text=_("Frames Per Second (FPS)"),
    )


def BrightnessField():
    """Create a form field for brightness adjustment."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="!isNaN(parseFloat(value))",
            current_value=str(1.0),
            _name="brightness",
            _type="number",
            step="0.1",
            help=_("Adjust brightness level. Default is 1.0. Values >1.0 increase brightness, <1.0 decrease."),
        ),
        label_text=_("Brightness"),
    )


def ContrastField():
    """Create a form field for contrast adjustment."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="!isNaN(parseFloat(value))",
            current_value=str(1.0),
            _name="contrast",
            _type="number",
            step="0.1",
            help=_("Adjust contrast level. Default is 1.0. Values >1.0 increase contrast, <1.0 decrease."),
        ),
        label_text=_("Contrast"),
    )


def ColorField():
    """Create a form field for color adjustment."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="!isNaN(parseFloat(value))",
            current_value=str(1.0),
            _name="color",
            _type="number",
            step="0.1",
            help=_("Adjust color saturation level. Default is 1.0. Values >1.0 increase saturation, <1.0 decrease."),
        ),
        label_text=_("Color Saturation"),
    )


def GammaField():
    """Create a form field for gamma adjustment."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="!isNaN(parseFloat(value))",
            current_value=str(1.0),
            _name="gamma",
            _type="number",
            step="0.1",
            help=_("Adjust gamma level. Default is 1.0. Values >1.0 increase gamma, <1.0 decrease."),
        ),
        label_text=_("Gamma"),
    )


def SharpnessField():
    """Create a form field for sharpness adjustment."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="!isNaN(parseFloat(value))",
            current_value=str(1.0),
            _name="sharpness",
            _type="number",
            step="0.1",
            help=_("Adjust sharpness level. Default is 1.0. Values >1.0 increase sharpness, <1.0 decrease."),
        ),
        label_text=_("Sharpness"),
    )


def RotationField():
    """Create a form field for video rotation selection."""
    return FormFieldHorizontal(
        FormFieldSelect(
            *[
                (str(angle), f"{angle}°")
                for angle in [-90, 0, 90, 180]
            ],
            current_value=str(0),
            _name="rotation",
            help=_("Select the rotation angle."),
        ),
        label_text=_("Rotation"),
    )


def MirrorAxisField():
    """Create a form field for video/audio/image mirroring axis selection."""
    return FormFieldHorizontal(
        FormFieldSelect(
            *[
                ("", _("No change")),
                ("x", _("Horizontal")),
                ("y", _("Vertical")),
            ],
            current_value="",
            _name="mirror-axis",
            help=_("Select the axis to mirror the video."),
        ),
        label_text=_("Mirror Axis"),
    )


def DeshakeField():
    """Create a form field for deshake option."""
    return FormFieldCheckbox(
        current_value="off",
        _name="deshake",
        help=_("Enable video deshaking to reduce camera shake effects."),
        label_text=_("Deshake"),
    )


def UnsharpField():
    """Create a form field for unsharp option."""
    return FormFieldCheckbox(
        current_value="off",
        _name="unsharp",
        help=_("Enable unsharp filter to enhance video sharpness."),
        label_text=_("Unsharp"),
    )


__all__ = [
    "TargetSizeField",
    "AudioBitrateField",
    "VideoBitrateField",
    "AudioCodecField",
    "VideoCodecField",
    "VideoEncodingSpeedField",
    "VideoQualityField",
    "ResolutionField",
    "FPSField",
    "BrightnessField",
    "ContrastField",
    "ColorField",
    "GammaField",
    "SharpnessField",
    "RotationField",
    "MirrorAxisField",
    "DeshakeField",
    "UnsharpField",
]
