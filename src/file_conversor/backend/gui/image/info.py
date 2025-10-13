# src/file_conversor/backend/gui/image/info.py

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


def image_info():
    return render_template(
        'image/info.jinja2',
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Image"),
                'url': url_for('image_index'),
            },
            {
                'label': _("Info"),
                'url': url_for('image_info'),
                'active': True,
            },
        ],
    )
