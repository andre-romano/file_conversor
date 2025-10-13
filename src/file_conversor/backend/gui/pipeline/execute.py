# src/file_conversor/backend/gui/pipeline/execute.py

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


def pipeline_execute():
    return render_template(
        'pipeline/execute.jinja2',
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Pipeline"),
                'url': url_for('pipeline_index'),
            },
            {
                'label': _("Execute"),
                'url': url_for('pipeline_execute'),
                'active': True,
            },
        ],
    )
