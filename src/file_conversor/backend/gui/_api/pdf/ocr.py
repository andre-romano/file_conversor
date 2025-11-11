# src/file_conversor/backend/gui/_api/pdf/ocr.py

from flask import json, render_template, request, url_for
from pathlib import Path
from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi
from file_conversor.backend.gui.flask_api_status import FlaskApiStatus

from file_conversor.backend.pdf import OcrMyPDFBackend

from file_conversor.utils import CommandManager, ProgressManager

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation
from file_conversor.utils.rich_utils import get_progress_bar

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def _api_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """Thread to handle PDF OCR."""
    logger.debug(f"PDF page OCR thread received: {params}")
    input_files: list[Path] = [Path(i) for i in params['input-files']]
    output_dir: Path = Path(params['output-dir'])

    languages = [str(params['pdf-language'])]

    logger.info(f"[bold]{_('Performing OCR on PDF pages')}[/]...")
    ocrmypdf_backend = OcrMyPDFBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE['verbose'],
    )
    local_langs: set[str] = ocrmypdf_backend.get_available_languages()
    remote_langs: set[str] = set()

    install_langs = set(languages) - local_langs
    if install_langs:
        remote_langs = ocrmypdf_backend.get_available_remote_languages()
        if install_langs - remote_langs:
            print(f"{_('Available remote languages')}: {', '.join(remote_langs)}")
            print(f"{_('Languages requested')}: {', '.join(install_langs)}")
            raise ValueError(f"{_('Some languages are not available for installation')}.")

        with get_progress_bar() as progress:
            for lang in install_langs:
                task = progress.add_task(f"{_('Installing language')} '{lang}' ...", total=100)
                ocrmypdf_backend.install_language(
                    lang=lang,
                    progress_callback=lambda p: progress.update(task, completed=p),
                )
                progress.update(task, completed=100)

    for input_file in input_files:
        input_file = Path(input_file).resolve()
        output_file = output_dir / CommandManager.get_output_file(input_file, stem="_ocr")
        if not STATE["overwrite-output"] and output_file.exists():
            raise FileExistsError(f"{_("File")} '{output_file}' {_("exists")}. {_("Use")} 'file_conversor -oo' {_("to overwrite")}.")

        print(f"Processing '{output_file}' ...")

        ocrmypdf_backend.to_pdf(
            input_file=input_file,
            output_file=output_file,
            languages=languages,
        )

    logger.debug(f"{status}")


def api_pdf_ocr():
    """API endpoint to OCR PDF pages."""
    logger.info(f"[bold]{_('PDF page OCR requested via API.')}[/]")
    return FlaskApi.execute_response(_api_thread)
