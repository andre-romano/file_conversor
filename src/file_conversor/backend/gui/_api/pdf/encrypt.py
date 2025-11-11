# src/file_conversor/backend/gui/_api/pdf/encrypt.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.pdf import PyPDFBackend

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
    """Thread to handle PDF encryption."""
    logger.debug(f"PDF encryption thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_dir: Path = Path(params['output-dir'])

    encrypt_algo: str = str(params['pdf-encryption-algorithm'])
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

    logger.info(f"[bold]{_('Encrypting PDF files')}[/]...")
    pypdf_backend = PyPDFBackend(verbose=STATE["verbose"])

    def callback(input_file: Path, output_file: Path, progress_mgr: ProgressManager):
        pypdf_backend.encrypt(
            # files
            input_file=input_file,
            output_file=output_file,

            # passwords
            owner_password=owner_password,
            user_password=user_password,

            # permissions
            permission_annotate=allow_annotations,
            permission_fill_forms=allow_fill_forms,
            permission_modify=allow_modify,
            permission_modify_pages=allow_modify_pages,
            permission_copy=allow_copy,
            permission_accessibility=allow_accessibility,
            permission_print_low_quality=allow_print_lq,
            permission_print_high_quality=allow_print_hq,

            encryption_algorithm=PyPDFBackend.EncryptionAlgorithm.from_str(encrypt_algo),
            progress_callback=lambda p: status.set_progress(progress_mgr.update_progress(p)),
        )
        progress_mgr.complete_step()
    cmd_mgr = CommandManager(input_files, output_dir=output_dir, overwrite=STATE["overwrite-output"])
    cmd_mgr.run(callback, out_stem="_encrypted")

    logger.debug(f"{status}")


def api_pdf_encrypt():
    """API endpoint to encrypt PDF documents."""
    logger.info(f"[bold]{_('PDF encryption requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
