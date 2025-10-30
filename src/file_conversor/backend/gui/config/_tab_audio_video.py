# src/file_conversor/backend/gui/config/_tab_audio_video.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.audio_video import FFmpegBackend

from file_conversor.utils.dominate_bulma import *

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation, AVAILABLE_LANGUAGES

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def TabConfigAudioVideo() -> tuple | list:
    return (
        FormFieldHorizontal(
            FormFieldInput(
                validation_expr="Number.parseInt(value) >= 0",
                current_value=CONFIG['audio-bitrate'],
                _name="audio-bitrate",
                _type="number",
                help=_("Set the default audio bitrate (in kbps) for audio / video conversions. Type 0 to keep original audio bitrate."),
            ),
            label_text=_("Audio Bitrate (kbps)"),
        ),
        FormFieldHorizontal(
            FormFieldInput(
                validation_expr="Number.parseInt(value) >= 0",
                current_value=CONFIG['video-bitrate'],
                _name="video-bitrate",
                _type="number",
                help=_("Set the default video bitrate (in kbps) for video conversions. Type 0 to keep original video bitrate."),
            ),
            label_text=_("Video Bitrate (kbps)"),
        ),
        FormFieldHorizontal(
            FormFieldSelect(
                *[
                    (f, f.upper())
                    for f in filter(lambda x: x != 'null', FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)
                ],
                current_value=CONFIG['video-format'],
                _name="video-format",
                help=_("Select the desired video format for video conversions."),
            ),
            label_text=_("Video Format"),
        ),
        FormFieldHorizontal(
            FormFieldSelect(
                *[
                    (s, s.upper())
                    for s in FFmpegBackend.ENCODING_SPEEDS
                ],
                current_value=CONFIG['video-encoding-speed'],
                _name="video-encoding-speed",
                help=_("Select the encoding speed for video conversions. Faster speeds result in lower quality and higher file sizes."),
            ),
            label_text=_("Video Encoding Speed"),
        ),
        FormFieldHorizontal(
            FormFieldSelect(
                *[
                    (q, q.upper())
                    for q in FFmpegBackend.QUALITY_PRESETS
                ],
                current_value=CONFIG['video-quality'],
                _name="video-quality",
                help=_("Select the video quality for video conversions. Higher quality results in larger file sizes."),
            ),
            label_text=_("Video Quality"),
        ),
    )


__all__ = ['TabConfigAudioVideo']
