# src/file_conversor/backend/gui/video/index.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.video._dom_page import video_index_nav_item

from file_conversor.utils.dominate_bulma import PageCardGrid

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
            'image': url_for('icons', filename='convert.ico'),
            'title': _("Convert"),
            'subtitle': _("Convert a video file to another video format."),
            'url': url_for('video_convert'),
        },
        {
            'image': url_for('icons', filename='compress.ico'),
            'title': _("Compress"),
            'subtitle': _("Compress a video file to a target file size."),
            'url': url_for('video_compress'),
        },
        {
            'image': url_for('icons', filename='color.ico'),
            'title': _("Enhance"),
            'subtitle': _("Enhance video bitrate, resolution, fps, color, brightness, etc."),
            'url': url_for('video_enhance'),
        },
        {
            'image': url_for('icons', filename='left_right.ico'),
            'title': _("Mirror / Flip"),
            'subtitle': _("Mirror a video file (vertically or horizontally)."),
            'url': url_for('video_mirror'),
        },
        {
            'image': url_for('icons', filename='rotate_right.ico'),
            'title': _("Rotate"),
            'subtitle': _("Rotate a video file (clockwise or anti-clockwise)."),
            'url': url_for('video_rotate'),
        },
        {
            'image': url_for('icons', filename='resize.ico'),
            'title': _("Resize"),
            'subtitle': _("Resize video resolution (downscaling / upscaling)."),
            'url': url_for('video_resize'),
        },
        {
            'image': url_for('icons', filename='check.ico'),
            'title': _("Check"),
            'subtitle': _("Checks a audio/video file for corruption / inconsistencies."),
            'url': url_for('video_check'),
        },
        {
            'image': url_for('icons', filename='info.ico'),
            'title': _("Get info"),
            'subtitle': _("Get information about a audio/video file."),
            'url': url_for('video_info'),
        },
    ]
    return render_template_string(str(
        PageCardGrid(
            *tools,
            nav_items=[
                home_nav_item(),
                video_index_nav_item(active=True),
            ],
            _title=f"{_('Video Tools')} - File Conversor",
        )
    ))
