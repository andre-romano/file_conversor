# src/file_conversor/backend/gui/doc/index.py

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


def doc_index():
    tools = [
        {
            'media': {
                'image': {'src': url_for('icons', filename='convert.ico')},
                'title': _("Convert files"),
                'subtitle': _("Convert document files into other formats (requires Microsoft Word / LibreOffice)."),
            },
            'url': url_for('doc_convert'),
        },
    ]
    return render_template(
        'doc/index.jinja2',
        tools=tools,
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Document"),
                'url': url_for('doc_index'),
                'active': True,
            },
        ],
    )
