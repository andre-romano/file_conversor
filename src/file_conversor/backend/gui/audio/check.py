# src/file_conversor/backend/gui/audio/check.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.audio_video import FFmpegBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.audio._dom_page import audio_check_nav_item, audio_index_nav_item

from file_conversor.utils.bulma_utils import InputFilesField
from file_conversor.utils.dominate_bulma import PageForm

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageAudioCheck():
    return PageForm(
        InputFilesField(
            *[f for f in FFmpegBackend.SUPPORTED_IN_AUDIO_FORMATS],
            description=_("Audio files"),
        ),
        api_endpoint=f"{url_for('api_audio_check')}",
        nav_items=[
            home_nav_item(),
            audio_index_nav_item(),
            audio_check_nav_item(active=True),
        ],
        _title=f"{_('Audio Check')} - File Conversor",
    )


def audio_check():
    return render_template_string(str(
        PageAudioCheck()
    ))


__all__ = ['audio_check']
