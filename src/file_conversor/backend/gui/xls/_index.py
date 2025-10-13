# src/file_conversor/backend/gui/xls/index.py

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


def xls_index():
    tools = [
        {
            'media': {
                'image': {'src': url_for('icons', filename='convert.ico')},
                'title': _("Convert"),
                'subtitle': _("Convert spreadsheet files into other formats (requires Microsoft Word / LibreOffice)."),
            },
            'url': url_for('xls_convert'),
        },
    ]
    return render_template(
        'xls/index.jinja2',
        tools=tools,
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Spreadsheet"),
                'url': url_for('xls_index'),
                'active': True,
            },
        ],
    )
