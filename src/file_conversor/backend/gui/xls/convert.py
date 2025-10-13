# src/file_conversor/backend/gui/xls/convert.py

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


def xls_convert():
    return render_template(
        'xls/convert.jinja2',
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Spreadsheet"),
                'url': url_for('xls_index'),
            },
            {
                'label': _("Convert"),
                'url': url_for('xls_convert'),
                'active': True,
            },
        ],
    )
