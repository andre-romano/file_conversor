# src/file_conversor/backend/gui/text/compress.py

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


def text_compress():
    return render_template(
        'text/compress.jinja2',
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Text"),
                'url': url_for('text_index'),
            },
            {
                'label': _("Compress"),
                'url': url_for('text_compress'),
                'active': True,
            },
        ],
    )
