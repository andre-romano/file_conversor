# src\file_conversor\backend\gui\_api\component\modal.py

from flask import json, request, render_template, url_for

# user-provided modules
from file_conversor.utils.dominate_bulma import ModalCard

from file_conversor.backend.gui.flask_api import FlaskApi

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def api_component_modal():
    """API endpoint to show a modal."""
    logger.info(f"[bold]{_('Modal requested via API.')}[/]")
    args = FlaskApi.get_args()
    logger.debug(f"{args}")

    title = args.get('title', '')
    msg = args.get('msg', '')
    closeable = args.get('closeable', False)

    return str(
        ModalCard(
            msg,
            _title=title,
            closeable=closeable,
            _class_head="p-5",
            _class_body="p-5",
            _class_foot="p-5",
        )
    ), 200
