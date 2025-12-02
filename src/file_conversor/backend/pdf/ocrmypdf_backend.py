# src\file_conversor\backend\ocrmypdf_backend.py

import multiprocessing
import re
import ocrmypdf

from pathlib import Path

from typing import Any, Callable

# user-provided imports
from file_conversor.config import Environment, Log, State
from file_conversor.config.locale import get_translation

from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.backend.git_backend import GitBackend
from file_conversor.backend.http_backend import HttpBackend

from file_conversor.dependency import BrewPackageManager, ScoopPackageManager

STATE = State.get_instance()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()


class OcrMyPDFBackend(AbstractBackend):
    TESSDATA_DIR: Path | None = None

    TESSDATA_REPOSITORY = {
        "user_name": "tesseract-ocr",
        "repo_name": "tessdata",
        "branch": "main",
    }

    SUPPORTED_IN_FORMATS = {
        "pdf": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "pdf": {},
    }
    EXTERNAL_DEPENDENCIES = {
        "tesseract",
    }

    def __init__(
        self,
        install_deps: bool | None,
        verbose: bool = False,
    ):
        """
        Initialize the backend.

        :param install_deps: Install external dependencies. If True auto install using a package manager. If False, do not install external dependencies. If None, asks user for action. 

        :raises RuntimeError: if dependency is not found
        """
        super().__init__(
            pkg_managers={
                ScoopPackageManager({
                    "tesseract": "tesseract",
                }),
                BrewPackageManager({
                    "tesseract": "tesseract"
                }),
            },
            install_answer=install_deps,
        )
        self._install_deps = install_deps
        self._verbose = verbose

        self._tesseract_bin = self.find_in_path("tesseract")

        self.TESSDATA_DIR = self.get_tessdata_dir()
        logger.debug(f"{_('Tesseract tessdata directory')}: {self.TESSDATA_DIR}")

    def install_language(
            self,
            lang: str,
            progress_callback: Callable[[float], None] | None = None,
    ):
        if not self.TESSDATA_DIR:
            raise FileNotFoundError(_("Tessdata directory not found."))

        lang_file = self.TESSDATA_DIR / f"{lang}.traineddata"
        if lang_file.exists():
            logger.warning(f"{_('Language')} '{lang}' {_('already installed')}.")
            return

        lang_url = GitBackend.get_download_url(
            **self.TESSDATA_REPOSITORY,
            file_path=f"{lang}.traineddata",
        )
        http_backend = HttpBackend.get_instance(verbose=self._verbose)
        http_backend.download(
            url=lang_url,
            dest_file=lang_file,
            progress_callback=progress_callback,
        )

        available_languages = self.get_available_languages()
        if lang not in available_languages:
            raise RuntimeError(f"{_('Failed to install language')} '{lang}'.")

    def get_tessdata_dir(self) -> Path:
        """
        Get the tessdata directory.

        :return: Path to tessdata directory.

        :raises FileNotFoundError: if tessdata directory not found
        """
        if self.TESSDATA_DIR:
            return self.TESSDATA_DIR

        process = Environment.run(
            str(self._tesseract_bin),
            "--list-langs",
        )
        lines: list[str] = process.stdout.splitlines()
        for line in lines:
            match = re.match(r"^List of available languages in \"(.+)\"", line)
            if not match:
                continue
            tessdata_path = Path(match.group(1).strip()).resolve()
            if not tessdata_path.exists():
                raise FileNotFoundError(f"Tessdata path '{tessdata_path}' does not exist.")
            return tessdata_path
        raise FileNotFoundError(_("Tessdata directory not found."))

    def get_available_remote_languages(self) -> set[str]:
        """
        Get available remote languages for OCR.
        """
        remote_langs = set()
        for file_info in GitBackend.get_info_api(
            **self.TESSDATA_REPOSITORY,
        ):
            if not file_info.get("name", "").endswith(".traineddata"):
                continue
            lang = file_info["name"][:-len(".traineddata")]
            if lang and lang not in ("configs", "tessdata_best", "tessdata_fast"):
                remote_langs.add(lang)
        return remote_langs

    def get_available_languages(self) -> set[str]:
        """
        Get available languages for OCR.

        :return: List of available languages.
        """
        process = Environment.run(
            str(self._tesseract_bin),
            "--list-langs",
        )
        # First line is usually 'List of available languages (x):'
        langs: set[str] = set()
        for line in process.stdout.splitlines()[1:]:
            line = str(line).strip().lower()
            if not line or line == "none" or line.startswith("list of available"):
                continue
            langs.add(line)
        return langs

    def to_pdf(
        self,
        output_file: str | Path,
        input_file: str | Path,
        languages: list[str],
        num_processses: int = multiprocessing.cpu_count(),
    ):
        """
        OCR input files into output file.

        :param output_file: Output file
        :param input_file: Input file. 
        :param languages: Languages to use in OCR
        :param num_processes: Number of processes to use. Defaults to max number of CPU cores.

        :raises FileNotFoundError: if input file not found
        """
        input_file = Path(input_file).resolve()
        output_file = Path(output_file).resolve()

        self.check_file_exists(input_file)

        ocrmypdf.ocr(
            input_file=input_file,
            output_file=output_file,
            language=languages,
            jobs=max(1, num_processses),
            use_threads=False,  # use processes instead of threads due to GIL
            skip_text=True,  # skip OCR if text is already present
            progress_bar=True,
        )


__all__ = [
    "OcrMyPDFBackend",
]
