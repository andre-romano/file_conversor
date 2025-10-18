# src/file_conversor/backend/gui/doc/convert.py

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


def doc_convert():
    return render_template(
        'doc/convert.jinja2',
        breadcrumb_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Document Tools"),
                'url': url_for('doc_index'),
            },
            {
                'label': _("Convert"),
                'url': url_for('doc_convert'),
                'active': True,
            },
        ],
        doc_convert={
            'modal': {
                'title': _('Conversion error'),
                'error': _('An error occurred during the document conversion process:'),
            },
            'execute_btn': _('Execute'),
        }
    )
