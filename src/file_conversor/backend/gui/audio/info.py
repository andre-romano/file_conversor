# src/file_conversor/backend/gui/audio/info.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.audio_video import FFmpegBackend

from file_conversor.utils.bulma_utils import *
from file_conversor.utils.dominate_bulma import *

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageAudioInfo():
    return PageForm(
        InputFilesField(
            *[f for f in FFmpegBackend.SUPPORTED_IN_AUDIO_FORMATS],
            description=_("Audio files"),
        ),
        api_endpoint=f"{url_for('api_audio_info')}",
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
                'label': _("Info"),
                'url': url_for('audio_info'),
                'active': True,
            },
        ],
        _title=f"{_('Audio Info')} - File Conversor",
    )


def audio_info():
    return render_template_string(str(
        PageAudioInfo()
    ))
