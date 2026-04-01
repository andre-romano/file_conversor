
# src\file_conversor\command\pdf\ocr_cmd.py

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, override

from file_conversor.backend.pdf import OcrMyPDFBackend

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
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


PdfOcrExternalDependencies: set[str] = OcrMyPDFBackend.EXTERNAL_DEPENDENCIES

PdfOcrInFormats = OcrMyPDFBackend.SupportedInFormats
PdfOcrOutFormats = OcrMyPDFBackend.SupportedOutFormats


@dataclass(frozen=True)
class PdfOcrLanguageModel:
    code: str
    name: str


class PdfOcrCommand(AbstractCommand[PdfOcrInFormats, PdfOcrOutFormats]):
    input_files: list[Path]
    languages: list[str]
    output_dir: Path
    _install_step_completed: bool = False

    @classmethod
    @override
    def _external_dependencies(cls):
        return PdfOcrExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PdfOcrInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PdfOcrOutFormats

    @classmethod
    def get_available_remote_languages(cls) -> set[PdfOcrLanguageModel]:
        return {
            PdfOcrLanguageModel(code=lang, name=get_language_name(lang))
            for lang in OcrMyPDFBackend.get_available_remote_languages()
        }

    def get_installed_languages(self) -> set[PdfOcrLanguageModel]:
        backend = self._get_backend()
        return {
            PdfOcrLanguageModel(code=lang, name=get_language_name(lang))
            for lang in backend.get_installed_languages()
        }

    def _get_not_installed_languages(self) -> set[str]:
        backend = self._get_backend()
        local_langs = backend.get_installed_languages()
        to_install_langs = set(self.languages) - local_langs
        return to_install_langs

    def _get_backend(self) -> OcrMyPDFBackend:
        return OcrMyPDFBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )

    @override
    def execute(self):
        backend = self._get_backend()

        batch_datamodel = BatchFilesDataModel(
            input_files=self.input_files,
            output_dir=self.output_dir,
            overwrite_output=STATE.overwrite_output.enabled,
            out_stem="_ocr",
        )

        def step_one(data: FileDataModel, get_progress: Callable[[float], float]):
            # avoid assert errors for step two by copying input to output
            data.output_file.write_bytes(data.input_file.read_bytes())
            if self._install_step_completed:
                return

            to_install_langs = self._get_not_installed_languages()
            if not to_install_langs:
                self.progress_callback(get_progress(100.0))
                return

            remote_langs = backend.get_available_remote_languages()
            if to_install_langs - remote_langs:
                logger.info(f"{_('Available remote languages')}: {', '.join(remote_langs)}")
                logger.info(f"{_('Languages requested')}: {', '.join(to_install_langs)}")
                raise ValueError(f"{_('Some languages are not available for installation')}.")

            for idx, lang in enumerate(to_install_langs, start=1):
                logger.info(f"{_('Installing language')} '{lang}' ...")
                backend.install_language(
                    lang=lang,
                    progress_callback=lambda p, idx=idx: self.progress_callback(
                        get_progress((p * 100.0 * (idx - 1)) / len(to_install_langs))
                    ),
                )
            to_install_langs = self._get_not_installed_languages()
            if to_install_langs:
                raise RuntimeError(f"{_('Failed to install languages')}: {', '.join(to_install_langs)}")
            self._install_step_completed = True

        def step_two(data: FileDataModel, get_progress: Callable[[float], float]):
            logger.info(f"OCR file '{data.output_file}' ...")
            backend.to_pdf(
                input_file=data.input_file,
                output_file=data.output_file,
                languages=self.languages,
            )
            self.progress_callback(get_progress(100.0))

        batch_datamodel.execute(step_one, step_two)
        logger.info(f"{_('File OCR')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "PdfOcrExternalDependencies",
    "PdfOcrInFormats",
    "PdfOcrOutFormats",
    "PdfOcrLanguageModel",
    "PdfOcrCommand",
]
