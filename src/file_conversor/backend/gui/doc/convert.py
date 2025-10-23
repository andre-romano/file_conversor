# src/file_conversor/backend/gui/doc/convert.py

from typing import Any
from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.utils.dominate_bulma import *

from file_conversor.backend.office import DOC_BACKEND

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def doc_convert_bak():
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


def PageConvert(
    *items: dict[str, Any],
):
    return PageForm(
        FormFileList(
            input_name="input_files",
            validation_expr="value.length > 0",
            label_text=_("Input Files"),
            help_text=_("Select (or drag) the input files."),
        ),
        FormFieldHorizontal(
            FormFieldSelect(
                *[
                    (f, f.upper())
                    for f in DOC_BACKEND.SUPPORTED_OUT_FORMATS
                ],
                current_value="pdf",
                _name="output_format",
                help=_("Select the desired output format for the converted document."),
            ),
            label_text=_("Output Format"),
        ),
        FormFieldHorizontal(
            FormFieldOutputDirectory(
                _name="output_dir",
                help=_("Select the directory where the converted document will be saved."),
            ),
            label_text=_("Output Directory"),
        ),
        FormFieldCheckbox(
            current_value=STATE["overwrite-output"],
            _name="overwrite",
            label_text=_("Overwrite Existing Files"),
            help=_("Allow overwriting of existing files."),
        ),
        api_endpoint=f"{url_for('api_doc_convert')}",
        nav_items=[
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
        _title=_("File Conversor - Convert Doc"),
    )


def doc_convert():
    items = []
    # TODO

    return render_template_string(str(
        PageConvert(
            *items
        )
    ))
