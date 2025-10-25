# src\file_conversor\backend\gui\_api\component\modal.py

from flask import json, request, render_template, url_for

# user-provided modules
from file_conversor.utils.dominate_bulma import ModalCard

from file_conversor.backend.gui.web_app import WebApp

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

    args = WebApp.get_args()

    title = args.get('title')
    msg = args.get('msg')
    closeable = args.get('closeable', 'false')

    if title is None or msg is None:
        return _("Missing 'title' or 'msg' parameter."), 400

    return str(
        ModalCard(
            _title=title,
            content=msg,
            closeable=True if closeable.lower() == 'true' else False,
            _class_head="p-5",
            _class_body="p-5",
            _class_foot="p-5",
        )
    ), 200
