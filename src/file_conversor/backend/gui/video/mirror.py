# src/file_conversor/backend/gui/video/mirror.py

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


def video_mirror():
    return render_template(
        'video/mirror.jinja2',
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Video"),
                'url': url_for('video_index'),
            },
            {
                'label': _("Mirror"),
                'url': url_for('video_mirror'),
                'active': True,
            },
        ],
    )
