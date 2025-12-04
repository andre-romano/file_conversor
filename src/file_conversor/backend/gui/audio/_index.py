# src/file_conversor/backend/gui/audio/index.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.audio._dom_page import audio_index_nav_item

from file_conversor.utils.dominate_bulma import PageCardGrid

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def audio_index():
    tools = [
        {
            'image': url_for('icons', filename='check.ico'),
            'title': _("Check files"),
            'subtitle': _("Checks a audio file for corruption / inconsistencies."),
            'url': url_for('audio_check'),
        },
        {
            'image': url_for('icons', filename='convert.ico'),
            'title': _("Convert files"),
            'subtitle': _("Convert a audio/video file to an audio format."),
            'url': url_for('audio_convert'),
        },
        {
            'image': url_for('icons', filename='info.ico'),
            'title': _("Get info"),
            'subtitle': _("Get information about a audio file."),
            'url': url_for('audio_info'),
        },
    ]

    return render_template_string(str(PageCardGrid(
        *tools,
        nav_items=[
            home_nav_item(),
            audio_index_nav_item(active=True),
        ],
        _title=f"{_('Audio Tools')} - File Conversor",
    )))


__all__ = ['audio_index']
