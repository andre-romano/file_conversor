# src/file_conversor/backend/gui/_api/doc/convert.py

from pathlib import Path
import shutil
import tempfile
import threading

from werkzeug.datastructures import FileStorage
from flask import json, render_template, request, url_for
from typing import Any

# user-provided modules
from file_conversor.backend.gui.web_app import WebApp
from file_conversor.backend.gui.flask_status import FlaskStatusCompleted, FlaskStatusError

from file_conversor.backend.office import DOC_BACKEND

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()

fapp = WebApp.get_instance()


def doc_convert_thread(params: dict[str, Any]) -> None:
    """Thread to handle document conversion."""
    logger.debug(f"Document conversion thread received: {params}")
    status = fapp.get_status(params['status_id'])
    status.set_progress(-1)  # indeterminate progress
    logger.debug(f"{status}")
    try:
        output_dir = Path(params['output_dir'])
        output_format: str = params['output_format']
        input_files, temp_dir = params['input_files']
        input_files: list[Path]
        temp_dir: Path

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
        status.set(FlaskStatusCompleted(id=status.get_id()))
    except Exception as e:
        logger.error(f"Error during document conversion: {repr(e)}")
        status.set(FlaskStatusError(
            id=status.get_id(),
            exception=repr(e),
            progress=status.get_progress(),
        ))
    # clean temp dir
    logger.debug(f"Cleaning temporary directory: {temp_dir}")
    shutil.rmtree(temp_dir)


def api_doc_convert():
    """API endpoint to convert documents."""
    logger.info(f"[bold]{_('Document conversion requested via API.')}[/]")
    data = fapp.get_form_data()
    data['status_id'] = fapp.add_status().get_id()
    data['input_files'] = fapp.get_files_list("input-files")  # matches formData key
    threading.Thread(target=doc_convert_thread, args=(data,), daemon=True).start()
    return json.dumps({
        'status': 'processing',
        'status_id': data['status_id'],
        'message': 'Document conversion in progress.',
    }), 200
