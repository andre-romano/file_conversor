# src/file_conversor/backend/gui/hash/check.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.hash_backend import HashBackend

from file_conversor.utils.bulma_utils import *
from file_conversor.utils.dominate_bulma import *

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageHashCheck():
    return PageForm(
        InputFilesField(
            *[f for f in HashBackend.SUPPORTED_IN_FORMATS],
            description=_("Hash files"),
        ),
        api_endpoint=f"{url_for('api_hash_check')}",
        nav_items=[
            {
                'label': _("Home"),
                'url': url_for('index'),
            },
            {
                'label': _("Hash"),
                'url': url_for('hash_index'),
            },
            {
                'label': _("Check"),
                'url': url_for('hash_check'),
                'active': True,
            },
        ],
        _title=f"{_('Hash Check')} - File Conversor",
    )


def hash_check():
    return render_template_string(str(
        PageHashCheck()
    ))
