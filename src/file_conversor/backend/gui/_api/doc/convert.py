# src/file_conversor/backend/gui/_api/doc/convert.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.office import DOC_BACKEND

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def doc_convert_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle document conversion."""
    logger.debug(f"Document conversion thread received: {params}")
    output_dir: Path = Path(params['output_dir'])
    output_format: str = params['output_format']
    input_files: list[Path] = [Path(i) for i in params['input_files']]

    files: list[tuple[Path | str, Path | str]] = [
        (input_path, output_dir / f"{input_path.stem}.{output_format}")
        for input_path in input_files
    ]
    total_files = len(files)

    logger.info(f"[bold]{_('Converting files')}[/]...")
    doc_backend = DOC_BACKEND(
        install_deps=CONFIG['install-deps'],
        verbose=STATE["verbose"],
    )
    doc_backend.convert(
        files=files,
        file_processed_callback=lambda _: status.set_progress(int(
            (status.get_progress() or 0) + (100.0 / total_files)
        )),
    )
    logger.debug(f"{status}")


def api_doc_convert():
    """API endpoint to convert documents."""
    logger.info(f"[bold]{_('Document conversion requested via API.')}[/]")
    return FlaskApi.execute_response(doc_convert_thread)
