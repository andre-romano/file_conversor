# src/file_conversor/backend/gui/config/index.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.backend.gui._dom_page import *
from file_conversor.backend.gui.config._dom_page import *

from file_conversor.backend.gui.config._tab_audio_video import TabConfigAudioVideo
from file_conversor.backend.gui.config._tab_general import TabConfigGeneral
from file_conversor.backend.gui.config._tab_image import TabConfigImage
from file_conversor.backend.gui.config._tab_network import TabConfigNetwork
from file_conversor.backend.gui.config._tab_pdf import TabConfigPDF

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

from file_conversor.utils.dominate_bulma import *

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def PageConfig():
    return PageForm(
        Tabs(
            {
                'label': _('General'),
                'icon': 'cog',
                'content': TabConfigGeneral(),
            },
            {
                'label': _('Network'),
                'icon': 'network-wired',
                'content': TabConfigNetwork(),
            },
            {
                'label': _('Audio & Video'),
                'icon': 'film',
                'content': TabConfigAudioVideo(),
            },
            {
                'label': _('Image'),
                'icon': 'image',
                'content': TabConfigImage(),
            },
            {
                'label': _('PDF'),
                'icon': 'file-pdf',
                'content': TabConfigPDF(),
            },
            active_tab=_('General'),
            _class="""
                is-toggle 
                is-toggle-rounded 
                is-flex 
                is-full-width 
                is-flex-direction-column 
                is-align-items-center
                mb-4
            """,
            _class_headers="mb-4",
            _class_content="is-full-width",
        ),
        api_endpoint=f"{url_for('api_config')}",
        nav_items=[
            home_nav_item(),
            config_index_nav_item(active=True),
        ],
        _title=_("Config - File Conversor"),
    )


def config_index():
    return render_template_string(str(
        PageConfig()
    ))
