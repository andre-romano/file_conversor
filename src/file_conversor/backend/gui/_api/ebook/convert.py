# src/file_conversor/backend/gui/_api/ebook/convert.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.ebook import CalibreBackend

from file_conversor.utils import CommandManager, ProgressManager

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle ebook conversion."""
    logger.debug(f"Ebook conversion thread received: {params}")
    input_files = [Path(i) for i in params['input-files']]
    format = str(params['file-format'])
    output_dir = Path(params['output-dir'])

    logger.info(f"[bold]{_('Converting files')}[/]...")
    backend = CalibreBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        logger.info(f"Processing '{output_file}' ... ")
        backend.convert(
            input_file=input_file,
            output_file=output_file,
        )
        status.set_progress(progress_mgr.complete_step())

    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_suffix=f".{format}")

    logger.debug(f"{status}")


def api_ebook_convert():
    """API endpoint to convert ebooks."""
    logger.info(f"[bold]{_('Ebook conversion requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
