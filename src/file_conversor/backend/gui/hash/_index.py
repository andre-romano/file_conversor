# src/file_conversor/backend/gui/hash/index.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.gui._dom_page import home_nav_item
from file_conversor.backend.gui.hash._dom_page import hash_index_nav_item

from file_conversor.utils.dominate_bulma import PageCardGrid

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def hash_index():
    tools = [
        {
            'image': url_for('icons', filename='check.ico'),
            'title': _("Check"),
            'subtitle': _("Checks a hash file (.sha256, .sha1, etc)."),
            'url': url_for('hash_check'),
        },
        {
            'image': url_for('icons', filename='new_file.ico'),
            'title': _("Create"),
            'subtitle': _("Creates a hash file (.sha256, .sha1, etc)."),
            'url': url_for('hash_create'),
        },
    ]
    return render_template_string(str(
        PageCardGrid(
            *tools,
            nav_items=[
                home_nav_item(),
                hash_index_nav_item(active=True),
            ],
            _title=f"{_('Hash Tools')} - File Conversor",
        ))
    )


__all__ = [
    'hash_index',
]
