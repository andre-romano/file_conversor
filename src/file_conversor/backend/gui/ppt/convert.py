# src/file_conversor/backend/gui/ppt/convert.py

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


def ppt_convert():
    return render_template(
        'ppt/convert.jinja2',
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Presentation"),
                'url': url_for('ppt_index'),
            },
            {
                'label': _("Convert"),
                'url': url_for('ppt_convert'),
                'active': True,
            },
        ],
    )
