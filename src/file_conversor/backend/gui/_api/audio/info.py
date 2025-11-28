# src/file_conversor/backend/gui/_api/audio/info.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.audio_video import FFprobeBackend

from file_conversor.utils.backend import FFprobeParser
from file_conversor.utils.bulma_utils import *
from file_conversor.utils.dominate_utils import *

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()

EXTERNAL_DEPENDENCIES = FFprobeBackend.EXTERNAL_DEPENDENCIES


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle audio information retrieval."""
    logger.debug(f"Audio info thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]

    backend = FFprobeBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    with div() as result:
        for input_file in input_files:
            logger.info(f"[bold]{_('Retrieving info for')}[/] [green]{input_file.name}[/]...")
            parser = FFprobeParser(backend, input_file)
            parser.run()

            parser.get_chapters().div()
            parser.get_format().div()
            parser.get_streams().div()
            div("----------------------------------------")
            br()

    status.set_message(str(result))
    status.set_progress(100)
    logger.debug(f"{status}")


def api_audio_info():
    """API endpoint to get audio file information."""
    logger.info(f"[bold]{_('Audio info requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)


__all__ = [
    "EXTERNAL_DEPENDENCIES",
    "api_audio_info",
]
