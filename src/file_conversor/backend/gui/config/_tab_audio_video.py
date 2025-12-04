# src/file_conversor/backend/gui/config/_tab_audio_video.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.audio_video import FFmpegBackend

from file_conversor.utils.bulma_utils.audio_video import AudioBitrateField, VideoBitrateField, VideoEncodingSpeedField, VideoQualityField
from file_conversor.utils.dominate_bulma import FormFieldHorizontal, FormFieldSelect

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
        VideoEncodingSpeedField(),
        VideoQualityField(),
        AudioBitrateField(),
        VideoBitrateField(),
    )


__all__ = ['TabConfigAudioVideo']
