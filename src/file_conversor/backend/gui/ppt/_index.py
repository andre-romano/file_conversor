# src/file_conversor/backend/gui/ppt/index.py

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


def ppt_index():
    tools = [
        {
            'image': url_for('icons', filename='convert.ico'),
            'title': _("Convert files"),
            'subtitle': _("Convert presentation files into other formats (requires Microsoft Word / LibreOffice)."),
            'url': url_for('ppt_convert'),
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
                    'label': _("Presentation"),
                    'url': url_for('ppt_index'),
                    'active': True,
                },
            ],
            _title=_("File Conversor - Presentation Tools"),
        )
    ))
