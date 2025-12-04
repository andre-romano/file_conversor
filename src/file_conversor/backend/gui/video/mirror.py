# src/file_conversor/backend/gui/video/mirror.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.audio_video import FFmpegBackend

from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.video._dom_page import video_index_nav_item, video_mirror_nav_item

from file_conversor.utils.bulma_utils import AudioBitrateField, MirrorAxisField, VideoBitrateField, VideoEncodingSpeedField, VideoQualityField, FileFormatField, InputFilesField, OutputDirField

from file_conversor.utils.dominate_bulma import PageForm, Tabs

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def TabGeneral() -> list | tuple:
    return [
        InputFilesField(
            *[f for f in FFmpegBackend.SUPPORTED_IN_VIDEO_FORMATS],
            description=_("Video files"),
        ),
        FileFormatField(
            *[
                (q, q.upper())
                for q in filter(lambda x: x.lower() != 'null', FFmpegBackend.SUPPORTED_OUT_VIDEO_FORMATS)
            ],
            current_value='mp4',
        ),
        MirrorAxisField(),
        OutputDirField(),
    ]


def TabAdvanced() -> list | tuple:
    return [
        AudioBitrateField(),
        VideoBitrateField(),

        VideoEncodingSpeedField(),
        VideoQualityField(),
    ]


def PageVideoMirror():
    return PageForm(
        Tabs(
            {
                'label': _('General'),
                'icon': 'cog',
                'content': TabGeneral(),
            },
            {
                'label': _('Advanced'),
                'icon': 'tools',
                'content': TabAdvanced(),
            },
            active_tab=_('General'),
            _class="""
                is-toggle 
                is-toggle-rounded 
                is-flex 
                is-full-width 
                is-flex-direction-column 
                is-align-items-center
                mb-4
            """,
            _class_headers="mb-4",
            _class_content="is-full-width",
        ),
        api_endpoint=f"{url_for('api_video_mirror')}",
        nav_items=[
            home_nav_item(),
            video_index_nav_item(),
            video_mirror_nav_item(active=True),
        ],
        _title=f"{_('Video Mirror')} - File Conversor",
    )


def video_mirror():
    return render_template_string(str(
        PageVideoMirror()
    ))
