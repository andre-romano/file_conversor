# src/file_conversor/backend/gui/hash/create.py

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


def hash_create():
    return render_template(
        'hash/create.jinja2',
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Hash"),
                'url': url_for('hash_index'),
            },
            {
                'label': _("Create"),
                'url': url_for('hash_create'),
                'active': True,
            },
        ],
    )
