# src/file_conversor/backend/gui/text/index.py

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


def text_index():
    tools = [
        {
            'media': {
                'image': {'src': url_for('icons', filename='check.ico')},
                'title': _("Check files"),
                'subtitle': _("Checks a text file schema compliance (json, xml, yaml, etc)."),
            },
            'url': url_for('text_check'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='compress.ico')},
                'title': _("Compress / Minify"),
                'subtitle': _("Compress / minify text file formats (json, xml, yaml, etc)."),
            },
            'url': url_for('text_compress'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='convert.ico')},
                'title': _("Convert"),
                'subtitle': _("Converts text file formats (json, xml, yaml, etc)."),
            },
            'url': url_for('text_convert'),
        },
    ]
    return render_template(
        'text/index.jinja2',
        tools=tools,
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Text"),
                'url': url_for('text_index'),
                'active': True,
            },
        ],
    )
