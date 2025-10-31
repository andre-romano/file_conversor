# src/file_conversor/backend/gui/audio/check.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.audio_video.ffmpeg_backend import FFmpegBackend

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


def PageAudioCheck():
    return PageForm(
        FormFileList(
            input_name="input_files",
            validation_expr="value.length > 0",
            label_text=_("Input Files"),
            help_text=_("Select (or drag) the input files."),
            add_help=_("Add file"),
            remove_help=_("Remove file"),
            file_types=[
                format_file_types_webview(
                    *[f for f in FFmpegBackend.SUPPORTED_IN_AUDIO_FORMATS],
                    description=_("Audio files"),
                ),
            ],
            multiple=True,
        ),
        api_endpoint=f"{url_for('api_audio_check')}",
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
                'label': _("Check"),
                'url': url_for('audio_check'),
                'active': True,
            },
        ],
        _title=f"{_('Audio Check')} - File Conversor",
    )


def audio_check():
    return render_template_string(str(
        PageAudioCheck()
    ))
