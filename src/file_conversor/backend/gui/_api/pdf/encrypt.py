# src/file_conversor/backend/gui/_api/pdf/encrypt.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.cli.pdf.encrypt_cmd import execute_pdf_encrypt_cmd, PyPDFBackend

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()

EncryptionPermission = PyPDFBackend.EncryptionPermission


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF encryption."""
    logger.debug(f"PDF encryption thread received: {params}")
    input_files = [Path(i) for i in params['input-files']]
    output_dir = Path(params['output-dir'])

    encrypt_algo = str(params['pdf-encryption-algorithm'])
    owner_password = str(params['owner-password'])
    user_password = params['user-password'] or None

    permissions: list[EncryptionPermission] = [
        EncryptionPermission.NONE if not bool(params['annotate']) else EncryptionPermission.ANNOTATE,
        EncryptionPermission.NONE if not bool(params['fill_forms']) else EncryptionPermission.FILL_FORMS,
        EncryptionPermission.NONE if not bool(params['modify']) else EncryptionPermission.MODIFY,
        EncryptionPermission.NONE if not bool(params['modify_pages']) else EncryptionPermission.MODIFY_PAGES,
        EncryptionPermission.NONE if not bool(params['copy']) else EncryptionPermission.COPY,
        EncryptionPermission.NONE if not bool(params['accessibility']) else EncryptionPermission.ACCESSIBILITY,
        EncryptionPermission.NONE if not bool(params['print_lq']) else EncryptionPermission.PRINT_LQ,
        EncryptionPermission.NONE if not bool(params['print_hq']) else EncryptionPermission.PRINT_HQ,
    ]

    execute_pdf_encrypt_cmd(
        input_files=input_files,
        decrypt_password=None,
        owner_password=owner_password,
        user_password=user_password,
        permissions=permissions,
        encrypt_algo=encrypt_algo,
        output_dir=output_dir,
        progress_callback=status.set_progress,
    )


def api_pdf_encrypt():
    """API endpoint to encrypt PDF documents."""
    logger.info(f"[bold]{_('PDF encryption requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
