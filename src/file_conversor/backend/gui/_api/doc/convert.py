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

    total_files = len(input_files)
    for index, input_path in enumerate(input_files):
        logger.info(f"[bold]{_('Converting file')}[/]: {input_path.name}")

        # Perform conversion
        output_filename = input_path.with_suffix(f".{output_format}").name
        output_path = (output_dir / output_filename).resolve()

        doc_backend = DOC_BACKEND(
            install_deps=CONFIG['install-deps'],
            verbose=STATE["verbose"],
        )
        doc_backend.convert(
            input_file=input_path,
            output_file=output_path,
        )

        # Update status
        progress = int(((index + 1) / total_files) * 100)
        status.set_progress(progress)
        logger.debug(f"{status}")


def api_doc_convert():
    """API endpoint to convert documents."""
    logger.info(f"[bold]{_('Document conversion requested via API.')}[/]")
    return FlaskApi.execute_response(doc_convert_thread)
