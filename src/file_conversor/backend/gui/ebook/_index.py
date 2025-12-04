# src/file_conversor/backend/gui/ebook/index.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.ebook._dom_page import ebook_index_nav_item

from file_conversor.utils.dominate_bulma import PageCardGrid

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def ebook_index():
    tools = [
        {
            'image': url_for('icons', filename='convert.ico'),
            'title': _("Convert files"),
            'subtitle': _("Convert an ebook file to another ebook format (or PDF)."),
            'url': url_for('ebook_convert'),
        },
    ]
    return render_template_string(str(
        PageCardGrid(
            *tools,
            nav_items=[
                home_nav_item(),
                ebook_index_nav_item(active=True),
            ],
            _title=f"{_('Ebook Tools')} - File Conversor",
        )
    ))
