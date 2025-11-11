# src/file_conversor/backend/gui/_api/hash/create.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.hash_backend import HashBackend

from file_conversor.utils import CommandManager, ProgressManager
from file_conversor.utils.backend import FFprobeParser

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle hash creating."""
    logger.debug(f"Hash create thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_file = Path(params.get('output-file') or "")

    logger.info(f"[bold]{_('Creating hash files')}[/]...")
    backend = HashBackend(
        verbose=STATE["verbose"],
    )
    with ProgressManager() as progress_mgr:
        backend.generate(
            input_files=input_files,
            output_file=output_file,
            progress_callback=lambda p: status.set_progress(progress_mgr.update_progress(p)),
        )
        status.set_progress(progress_mgr.complete_step())

    logger.debug(f"{status}")


def api_hash_create():
    """API endpoint to create hash files."""
    logger.info(f"[bold]{_('Hash create requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
