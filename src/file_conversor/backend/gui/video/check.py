# src/file_conversor/backend/gui/video/check.py

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


def PageVideoCheck():
    return PageForm(
        InputFilesField(
            *[f for f in FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS],
            description=_("Video files"),
        ),
        api_endpoint=f"{url_for('api_video_check')}",
        nav_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Video"),
                'url': url_for('video_index'),
            },
            {
                'label': _("Check"),
                'url': url_for('video_check'),
                'active': True,
            },
        ],
        _title=f"{_('Video Check')} - File Conversor",
    )


def video_check():
    return render_template_string(str(
        PageVideoCheck()
    ))
