# src/file_conversor/backend/gui/pdf/repair.py

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


def pdf_repair():
    return render_template(
        'pdf/repair.jinja2',
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("PDF"),
                'url': url_for('pdf_index'),
            },
            {
                'label': _("Repair"),
                'url': url_for('pdf_repair'),
                'active': True,
            },
        ],
    )
