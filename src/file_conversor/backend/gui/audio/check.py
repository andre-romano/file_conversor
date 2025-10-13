# src/file_conversor/backend/gui/audio/check.py

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


def audio_check():
    return render_template(
        'audio/check.jinja2',
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Audio"),
                'url': url_for('audio_index'),
            },
            {
                'label': _("Check files"),
                'url': url_for('audio_check'),
                'active': True,
            },
        ],
    )
