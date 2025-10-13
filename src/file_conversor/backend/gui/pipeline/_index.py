# src/file_conversor/backend/gui/pipeline/index.py

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


def pipeline_index():
    tools = [
        {
            'media': {
                'image': {'src': url_for('icons', filename='new_file.ico')},
                'title': _("Create pipeline"),
                'subtitle': _("Creates a file processing pipeline (for tasks automation)."),
            },
            'url': url_for('pipeline_create'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='run.ico')},
                'title': _("Execute pipeline"),
                'subtitle': _("Executes a file processing pipeline."),
            },
            'url': url_for('pipeline_execute'),
        },
    ]
    return render_template(
        'pipeline/index.jinja2',
        tools=tools,
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Pipeline"),
                'url': url_for('pipeline_index'),
                'active': True,
            },
        ],
    )
