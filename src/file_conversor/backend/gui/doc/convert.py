# src/file_conversor/backend/gui/doc/convert.py

from flask import render_template, url_for

# user-provided modules
from file_conversor.backend.office import DOC_BACKEND

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
            'fields': {
                'input_files': {
                    'name': 'input-files',
                    'label': _('Input Files'),
                    'help': _('Select the document files you want to convert.'),
                    'validation': {
                        'form': "Alpine.store('form')",
                        'expr': 'value.length > 0',
                    }
                },
                'output_dir': {
                    'name': 'output_dir',
                    'label': _('Output Directory'),
                    'help': _('Select the directory where the converted document will be saved.'),
                    'validation': {
                        'form': "Alpine.store('form')",
                        'expr': 'true',
                    }
                },
                'output_format': {
                    'current': 'pdf',
                    'name': 'output_format',
                    'label': _('Output Format'),
                    'help': _('Select the desired output format for the converted document.'),
                    'options': DOC_BACKEND.SUPPORTED_OUT_FORMATS,
                },
                'overwrite': {
                    'current': False,
                    'name': 'overwrite',
                    'label': _('Overwrite Existing Files'),
                    'help': _('Allow overwriting of existing files.'),
                },
            },
            'modal': {
                'title': _('Conversion error'),
                'error': _('An error occurred during the document conversion process:'),
            },
            'execute_btn': _('Execute'),
        }
    )
