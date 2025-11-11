# src/file_conversor/backend/gui/_api/pdf/convert.py

from email.mime import image
from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.office import DOC_BACKEND
from file_conversor.backend.pdf import PyMuPDFBackend

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

    file_format: str = str(params['file-format'])
    image_dpi: int = int(params['image-dpi'])

    logger.info(f"[bold]{_('Converting PDF files')}[/]...")

    files: list[tuple[Path | str, Path | str]] = []
    for input_file in input_files:
        output_file = output_dir / CommandManager.get_output_file(input_file, suffix=f".{file_format}")
        if not STATE["overwrite-output"] and output_file.exists():
            raise FileExistsError(f"{_("File")} '{output_file}' {_("exists")}. {_("Use")} 'file_conversor -oo' {_("to overwrite")}.")
        files.append((input_file, output_file))

    if file_format in DOC_BACKEND.SUPPORTED_OUT_FORMATS:
        backend = DOC_BACKEND(
            install_deps=CONFIG['install-deps'],
            verbose=STATE['verbose'],
        )
    else:
        backend = PyMuPDFBackend(verbose=STATE['verbose'])

    with ProgressManager(len(input_files)) as progress_mgr:
        logger.info(f"[bold]{_('Converting files')}[/] ...")
        # Perform conversion
        if isinstance(backend, DOC_BACKEND):
            backend.convert(
                files=files,
                file_processed_callback=lambda _: status.set_progress(progress_mgr.complete_step())
            )
        elif isinstance(backend, PyMuPDFBackend):
            for input_file, output_file in files:
                backend.convert(
                    input_file=input_file,
                    output_file=output_file,
                    dpi=image_dpi,
                )
                status.set_progress(progress_mgr.complete_step())

    logger.debug(f"{status}")


def api_pdf_convert():
    """API endpoint to convert PDF documents."""
    logger.info(f"[bold]{_('PDF conversion requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
