# src/file_conversor/backend/gui/config/_tab_general.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.utils.dominate_bulma import *

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation, AVAILABLE_LANGUAGES

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def TabConfigGeneral() -> tuple | list:
    return (
        FormFieldHorizontal(
            FormFieldSelect(
                *[
                    (f, f.upper())
                    for f in AVAILABLE_LANGUAGES
                ],
                current_value=CONFIG['language'],
                _name="language",
                help=_("Select the desired language for the user interface."),
            ),
            label_text=_("Language"),
        ),
        FormFieldCheckbox(
            current_value=CONFIG['install-deps'],
            _name="install-deps",
            label_text=_('Automatic install of missing dependencies, on demand.'),
            help=_('If enabled, the application will attempt to automatically install any missing dependencies when needed.'),
        ),
    )


__all__ = ['TabConfigGeneral']
