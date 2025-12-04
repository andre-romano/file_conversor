# src/file_conversor/backend/gui/config/_tab_network.py

from flask import render_template, render_template_string, url_for

# user-provided modules
from file_conversor.utils.dominate_bulma import FormFieldHorizontal, FormFieldInput

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation, AVAILABLE_LANGUAGES

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def TabConfigNetwork() -> tuple | list:
    return (
        FormFieldHorizontal(
            FormFieldInput(
                validation_expr="Number.parseInt(value) >= 1 && Number.parseInt(value) <= 65535",
                current_value=CONFIG['port'],
                _name="port",
                _type="number",
                help=_("Set the port number for the application to listen on (1-65535)."),
            ),
            label_text=_("Port"),
        ),
    )


__all__ = ['TabConfigNetwork']
