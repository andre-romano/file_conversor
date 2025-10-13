# src/file_conversor/backend/gui/video/info.py

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


def video_info():
    return render_template(
        'video/info.jinja2',
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
                'label': _("Info"),
                'url': url_for('video_info'),
                'active': True,
            },
        ],
    )
