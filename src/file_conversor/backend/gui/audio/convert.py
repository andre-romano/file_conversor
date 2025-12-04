# src/file_conversor/backend/gui/audio/convert.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.audio_video import FFmpegBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.audio._dom_page import audio_convert_nav_item, audio_index_nav_item

from file_conversor.utils.bulma_utils import AudioBitrateField, FileFormatField, InputFilesField, OutputDirField
from file_conversor.utils.dominate_bulma import PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageAudioConvert():
    return PageForm(
        InputFilesField(
            *[f for f in FFmpegBackend.SUPPORTED_IN_FORMATS],
            description=_("Audio and Video files"),
        ),
        FileFormatField(*[
            (q, q.upper())
            for q in filter(lambda x: x.lower() != 'null', FFmpegBackend.SUPPORTED_OUT_AUDIO_FORMATS)
        ], current_value='mp3'),
        OutputDirField(),
        AudioBitrateField(),
        api_endpoint=url_for('api_audio_convert'),
        nav_items=[
            home_nav_item(),
            audio_index_nav_item(),
            audio_convert_nav_item(active=True),
        ],
        _title=f"{_('Audio Convert')} - File Conversor",
    )


def audio_convert():
    return render_template_string(str(
        PageAudioConvert()
    ))


__all__ = ['audio_convert']
