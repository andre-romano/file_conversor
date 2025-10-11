# src\file_conversor\backend\gui\index.py

from flask import render_template, send_from_directory, url_for

# user-provided modules
from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def index():
    tools = [
        # OFFICE
        {
            'media': {
                'image': {'src': url_for('icons', filename='doc.ico')},
                'title': _("Document Tools"),
                'subtitle': f"{_('Document file manipulation')} {_('(requires MS Office / LibreOffice)')})",
            },
            'url': url_for('doc_index'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='xls.ico')},
                'title': _("Spreadsheet Tools"),
                'subtitle': f"{_('Spreadsheet file manipulation')} {_('(requires MS Office / LibreOffice)')})",
            },
            'url': url_for('xls_index'),
        },
        {
            'media': {
                'image': {'src': url_for('icons', filename='ppt.ico')},
                'title': _("Presentation Tools"),
                'subtitle': f"{_('Presentation file manipulation')} {_('(requires MS Office / LibreOffice)')})",
            },
            'url': url_for('ppt_index'),
        },
        # PDF
        {
            'media': {
                'image': {'src': url_for('icons', filename='pdf.ico')},
                'title': _("PDF Tools"),
                'subtitle': _("Convert, Split, Merge, Compress and more."),
            },
            'url': url_for('pdf_index'),
        },
    ]
    return render_template('index.jinja2', tools=tools)
