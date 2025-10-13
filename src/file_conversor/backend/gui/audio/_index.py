# src/file_conversor/backend/gui/audio/index.py

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


def audio_index():
    tools = [
        {
            'media': {
                'image': {'src': url_for('icons', filename='check.ico')},
                'title': _("Check files"),
                'subtitle': _("Checks a audio file for corruption / inconsistencies."),
            },
            'url': url_for('audio_check'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='convert.ico')},
                'title': _("Convert files"),
                'subtitle': _("Convert a audio/video file to an audio format."),
            },
            'url': url_for('audio_convert'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='info.ico')},
                'title': _("Get info"),
                'subtitle': _("Get information about a audio file."),
            },
            'url': url_for('audio_info'),
        },
    ]
    return render_template(
        'audio/index.jinja2',
        tools=tools,
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Audio"),
                'url': url_for('audio_index'),
                'active': True,
            },
        ],
    )
