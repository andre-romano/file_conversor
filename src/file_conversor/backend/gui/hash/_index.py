# src/file_conversor/backend/gui/hash/index.py

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


def hash_index():
    tools = [
        {
            'media': {
                'image': {'src': url_for('icons', filename='check.ico')},
                'title': _("Check"),
                'subtitle': _("Checks a hash file (.sha256, .sha1, etc)."),
            },
            'url': url_for('hash_check'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='new_file.ico')},
                'title': _("Create"),
                'subtitle': _("Creates a hash file (.sha256, .sha1, etc)."),
            },
            'url': url_for('hash_create'),
        },
    ]
    return render_template(
        'hash/index.jinja2',
        tools=tools,
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Hash"),
                'url': url_for('hash_index'),
                'active': True,
            },
        ],
    )
