# src\file_conversor\backend\ocrmypdf_backend.py

from enum import Enum
from pathlib import Path
from typing import Any, Callable

from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.backend.git_backend import GitBackend
from file_conversor.backend.http_backend import HttpBackend

# user-provided imports
from file_conversor.config import Environment, Log, get_translation
from file_conversor.dependency import BrewPackageManager, ScoopPackageManager


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()


class OcrMyPDFBackend(AbstractBackend):
    TESSDATA_REPOSITORY = GitBackend.RepositoryDataModel(
        user_name="tesseract-ocr",
        repo_name="tessdata",
        branch="main",
    )

    class SupportedInFormats(Enum):
        PDF = "pdf"

    class SupportedOutFormats(Enum):
        PDF = "pdf"

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

        self._tessdata_dir = self.get_tessdata_dir()
        logger.debug(f"{_('Tesseract tessdata directory')}: {self._tessdata_dir}")

    def install_language(
            self,
            lang: str,
            progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        lang_file = self._tessdata_dir / f"{lang}.traineddata"
        if lang_file.exists():
            logger.warning(f"{_('Language')} '{lang}' {_('already installed')}.")
            return

        lang_url = GitBackend.get_download_url(
            repository=self.TESSDATA_REPOSITORY,
            file_path=Path(f"{lang}.traineddata"),
        )
        http_backend = HttpBackend(verbose=self._verbose)
        http_backend.download(
            url=lang_url,
            dest_file=lang_file,
            progress_callback=progress_callback,
        )

        available_languages = self.get_installed_languages()
        if lang not in available_languages:
            raise RuntimeError(f"{_('Failed to install language')} '{lang}'.")

    def get_tessdata_dir(self) -> Path:
        """
        Get the tessdata directory.

        :return: Path to tessdata directory.

        :raises FileNotFoundError: if tessdata directory not found
        """
        import re

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
        remote_langs: set[str] = set()
        for file_info in GitBackend.get_info_api(
            repository=self.TESSDATA_REPOSITORY,
        ):
            if not file_info.get("name", "").endswith(".traineddata"):
                continue
            lang: str = file_info["name"][:-len(".traineddata")]
            if lang and lang not in ("configs", "tessdata_best", "tessdata_fast"):
                remote_langs.add(lang)
        return remote_langs

    def get_installed_languages(self) -> set[str]:
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
            line_parsed = str(line).strip().lower()
            if not line_parsed or line_parsed == "none" or line_parsed.startswith("list of available"):
                continue
            langs.add(line_parsed)
        return langs

    def to_pdf(
        self,
        output_file: Path,
        input_file: Path,
        languages: list[str],
        num_processes: int = 0,
    ):
        """
        OCR input files into output file.

        :param output_file: Output file
        :param input_file: Input file. 
        :param languages: Languages to use in OCR
        :param num_processes: Number of processes to use. Defaults to 0 (max number of CPU cores).

        :raises FileNotFoundError: if input file not found
        """
        import os

        import ocrmypdf

        num_processes = num_processes if num_processes > 0 else max(1, os.cpu_count() or 1)

        ocrmypdf.ocr(  # pyright: ignore[reportUnknownMemberType]
            input_file=input_file.resolve(),
            output_file=output_file.resolve(),
            language=languages,
            jobs=num_processes,
            use_threads=False,  # use processes instead of threads due to GIL
            skip_text=True,  # skip OCR if text is already present
            progress_bar=True,
        )


__all__ = [
    "OcrMyPDFBackend",
]
