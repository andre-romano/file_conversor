# src/file_conversor/backend/gui/_api/pdf/encrypt.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.pdf.encrypt_cmd import execute_pdf_encrypt_cmd

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF encryption."""
    logger.debug(f"PDF encryption thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_dir: Path = Path(params['output-dir'])

    encrypt_algo: str = str(params['pdf-encryption-algorithm'])
    decrypt_password: str | None = params.get('decrypt-password')
    owner_password: str = str(params['owner-password'])
    user_password: str | None = str(params['user-password']) or None

    allow_annotations: bool = bool(params['allow-annotations'])
    allow_fill_forms: bool = bool(params['allow-fill-forms'])
    allow_modify: bool = bool(params['allow-modify'])
    allow_modify_pages: bool = bool(params['allow-modify-pages'])
    allow_copy: bool = bool(params['allow-copy'])
    allow_accessibility: bool = bool(params['allow-accessibility'])
    allow_print_lq: bool = bool(params['allow-print-lq'])
    allow_print_hq: bool = bool(params['allow-print-hq'])

    execute_pdf_encrypt_cmd(
        input_files=input_files,
        decrypt_password=decrypt_password,
        owner_password=owner_password,
        user_password=user_password,
        allow_annotate=allow_annotations,
        allow_fill_forms=allow_fill_forms,
        allow_modify=allow_modify,
        allow_modify_pages=allow_modify_pages,
        allow_copy=allow_copy,
        allow_accessibility=allow_accessibility,
        allow_print_lq=allow_print_lq,
        allow_print_hq=allow_print_hq,
        allow_all=False,
        encrypt_algo=encrypt_algo,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_pdf_encrypt():
    """API endpoint to encrypt PDF documents."""
    logger.info(f"[bold]{_('PDF encryption requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
