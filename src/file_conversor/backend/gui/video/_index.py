# src/file_conversor/backend/gui/video/index.py

from flask import render_template, url_for

# user-provided modules
from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def video_index():
    tools = [
        {
            'media': {
                'image': {'src': url_for('icons', filename='convert.ico')},
                'title': _("Convert"),
                'subtitle': _("Convert a video file to another video format."),
            },
            'url': url_for('video_convert'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='compress.ico')},
                'title': _("Compress"),
                'subtitle': _("Compress a video file to a target file size."),
            },
            'url': url_for('video_compress'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='color.ico')},
                'title': _("Enhance"),
                'subtitle': _("Enhance video bitrate, resolution, fps, color, brightness, etc."),
            },
            'url': url_for('video_enhance'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='left_right.ico')},
                'title': _("Mirror / Flip"),
                'subtitle': _("Mirror a video file (vertically or horizontally)."),
            },
            'url': url_for('video_mirror'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='rotate_right.ico')},
                'title': _("Rotate"),
                'subtitle': _("Rotate a video file (clockwise or anti-clockwise)."),
            },
            'url': url_for('video_rotate'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='resize.ico')},
                'title': _("Resize"),
                'subtitle': _("Resize video resolution (downscaling / upscaling)."),
            },
            'url': url_for('video_resize'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='check.ico')},
                'title': _("Check"),
                'subtitle': _("Checks a audio/video file for corruption / inconsistencies."),
            },
            'url': url_for('video_check'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='info.ico')},
                'title': _("Get info"),
                'subtitle': _("Get information about a audio/video file."),
            },
            'url': url_for('video_info'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='tasks.ico')},
                'title': _("List available codecs"),
                'subtitle': _("List available video formats and codecs."),
            },
            'url': url_for('video_list_formats'),
        }
    ]
    return render_template(
        'video/index.jinja2',
        tools=tools,
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Video"),
                'url': url_for('video_index'),
                'active': True,
            },
        ],
    )
