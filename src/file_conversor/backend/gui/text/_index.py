# src/file_conversor/backend/gui/text/index.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.utils.dominate_bulma import *

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def text_index():
    tools = [
        {
            'image': url_for('icons', filename='check.ico'),
            'title': _("Check files"),
            'subtitle': _("Checks a text file schema compliance (json, xml, yaml, etc)."),
            'url': url_for('text_check'),
        },
        {
            'image': url_for('icons', filename='compress.ico'),
            'title': _("Compress / Minify"),
            'subtitle': _("Compress / minify text file formats (json, xml, yaml, etc)."),
            'url': url_for('text_compress'),
        },
        {
            'image': url_for('icons', filename='convert.ico'),
            'title': _("Convert"),
            'subtitle': _("Converts text file formats (json, xml, yaml, etc)."),
            'url': url_for('text_convert'),
        },
    ]
    return render_template_string(str(
        PageCardGrid(
            *tools,
            nav_items=[
                {
                    'label': _("Home"),
                    'url': url_for('index'),
                },
                {
                    'label': _("Text"),
                    'url': url_for('text_index'),
                    'active': True,
                },
            ],
            _title=_("File Conversor - Text Tools"),
        )
    ))
