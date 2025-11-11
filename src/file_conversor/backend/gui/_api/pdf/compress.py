# src/file_conversor/backend/gui/_api/pdf/compress.py

import tempfile

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.pdf import GhostscriptBackend, PikePDFBackend

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
    """Thread to handle PDF compression."""
    logger.debug(f"PDF compression thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_dir: Path = Path(params['output-dir'])
    pdf_compression: str = str(params['pdf-compression'])

    pikepdf_backend = PikePDFBackend(verbose=STATE["verbose"])
    gs_backend = GhostscriptBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE['verbose'],
    )

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        with tempfile.TemporaryDirectory() as temp_dir:
            gs_out = Path(temp_dir) / CommandManager.get_output_file(input_file, stem="_gs")
            gs_backend.compress(
                input_file=input_file,
                output_file=gs_out,
                compression_level=GhostscriptBackend.Compression.from_str(pdf_compression),
                progress_callback=progress_mgr.update_progress
            )
            progress_mgr.complete_step()

            pikepdf_backend.compress(
                # files
                input_file=gs_out,
                output_file=output_file,
                progress_callback=progress_mgr.update_progress
            )
            progress_mgr.complete_step()
            print(f"Processing '{output_file}' ... OK")
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, steps=2, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_compressed")

    logger.debug(f"{status}")


def api_pdf_compress():
    """API endpoint to compress PDF documents."""
    logger.info(f"[bold]{_('PDF compression requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
