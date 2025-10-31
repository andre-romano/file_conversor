# src/file_conversor/backend/gui/audio/convert.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.audio_video import FFmpegBackend

from file_conversor.utils.bulma_utils import *
from file_conversor.utils.dominate_bulma import *
from file_conversor.utils.formatters import format_file_types_webview

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
            *[f for f in FFmpegBackend.SUPPORTED_IN_AUDIO_FORMATS],
            description=_("Audio files"),
        ),
        FileFormatField(*[
            (q, q.upper())
            for q in filter(lambda x: x.lower() != 'null', FFmpegBackend.SUPPORTED_OUT_AUDIO_FORMATS)
        ], current_value='mp3'),
        OutputDirField(),
        AudioBitrateField(),
        api_endpoint=url_for('api_audio_convert'),
        nav_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Audio"),
                'url': url_for('audio_index'),
            },
            {
                'label': _("Convert"),
                'url': url_for('audio_convert'),
                'active': True,
            },
        ],
        _title=f"{_('Audio Convert')} - File Conversor",
    )


def audio_convert():
    return render_template_string(str(
        PageAudioConvert()
    ))
