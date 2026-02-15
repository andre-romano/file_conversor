
# src\file_conversor\command\pdf\ocr_cmd.py

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.pdf import OcrMyPDFBackend

# user-provided modules
from file_conversor.command.data_models import BatchFilesDataModel, FileDataModel
from file_conversor.config import (
    Configuration,
    Log,
    State,
    get_language_name,
    get_translation,
)


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfOcrCommand:
    EXTERNAL_DEPENDENCIES: set[str] = OcrMyPDFBackend.EXTERNAL_DEPENDENCIES

    SupportedInFormats = OcrMyPDFBackend.SupportedInFormats
    SupportedOutFormats = OcrMyPDFBackend.SupportedOutFormats

    @dataclass(frozen=True)
    class LanguageModel:
        code: str
        name: str

    def __init__(self) -> None:
        super().__init__()
        self._backend = OcrMyPDFBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

    def get_installed_languages(self) -> set[LanguageModel]:
        return {
            self.LanguageModel(code=lang, name=get_language_name(lang))
            for lang in self._backend.get_installed_languages()
        }

    def get_available_remote_languages(self) -> set[LanguageModel]:
        return {
            self.LanguageModel(code=lang, name=get_language_name(lang))
            for lang in self._backend.get_available_remote_languages()
        }

    def install_languages(
        self,
        languages: list[str],
        progress_callback: Callable[[float], Any] = lambda p: p,
    ) -> None:
        local_langs = self._backend.get_installed_languages()

        install_langs = set(languages) - local_langs
        if not install_langs:
            progress_callback(100.0)
            return

        remote_langs = self._backend.get_available_remote_languages()
        if install_langs - remote_langs:
            logger.info(f"{_('Available remote languages')}: {', '.join(remote_langs)}")
            logger.info(f"{_('Languages requested')}: {', '.join(install_langs)}")
            raise ValueError(f"{_('Some languages are not available for installation')}.")

        for idx, lang in enumerate(install_langs, start=1):
            logger.info(f"{_('Installing language')} '{lang}' ...")
            self._backend.install_language(
                lang=lang,
                progress_callback=lambda p, idx=idx: progress_callback(
                    (p * 100.0 * (idx - 1)) / len(install_langs)
                ),
            )

    def ocr(
        self,
        input_files: list[Path],
        languages: list[str],
        output_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        installed_langs = self._backend.get_installed_languages()
        for lang in languages:
            if lang not in installed_langs:
                raise ValueError(f"{_('Language')} '{lang}' {_('is not installed. Installed languages')}: {', '.join(installed_langs)}")

        batch_datamodel = BatchFilesDataModel(
            input_files=input_files,
            output_dir=output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_ocr",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"OCR file '{data.output_file}' ...")
            self._backend.to_pdf(
                input_file=data.input_file,
                output_file=data.output_file,
                languages=languages,
            )
            progress_callback(get_progress(100.0))

        batch_datamodel.execute(step_one)
        logger.info(f"{_('File OCR')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "PdfOcrCommand",
]
