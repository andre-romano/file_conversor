# src\file_conversor\backend\ocrmypdf_backend.py

import multiprocessing
import re
import shutil
import tempfile
import ocrmypdf

from pathlib import Path

from typing import Any, Callable

# user-provided imports
from file_conversor.config import Environment, Log, State
from file_conversor.config.locale import get_translation

from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.backend.git_backend import GitBackend
from file_conversor.dependency import BrewPackageManager, ScoopPackageManager

STATE = State.get_instance()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()


class OcrMyPDFBackend(AbstractBackend):

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

        langs = self.get_available_languages()
        if not langs:
            logger.warning(f"{_('No Tesseract languages found. Installing language packs ...')}")
            self._install_tesseract_languages()
            if not self.get_available_languages():
                raise RuntimeError(_("No Tesseract languages found after installation."))
        logger.debug(f"{_('Available Tesseract languages')}: {', '.join(langs)}")

    def _install_tesseract_languages(self):
        tessdata_path = self.get_tessdata_dir()
        if not tessdata_path:
            raise RuntimeError(_("Could not determine Tesseract tessdata directory."))
        logger.info(f"{_('Tesseract tessdata directory')}: {tessdata_path}")

        git_backend = GitBackend(
            install_deps=self._install_deps,
            verbose=self._verbose,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            git_backend.clone(
                repo_url="https://github.com/tesseract-ocr/tessdata.git",
                dest_folder=temp_dir,
            )
            for src_file in Path(temp_dir).glob("*.traineddata"):
                dest_file = tessdata_path / src_file.name
                if dest_file.exists():
                    logger.warning(f"{_('Tesseract language file already exists')}: {dest_file}")
                    continue
                logger.debug(f"{_('Installing Tesseract language file')}: {dest_file}")
                Environment.move(src_file, dest_file)

    def get_tessdata_dir(self) -> Path:
        """
        Get the tessdata directory.

        :return: Path to tessdata directory.

        :raises FileNotFoundError: if tessdata directory not found
        """
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

    def get_available_languages(self) -> list[str]:
        """
        Get available languages for OCR.

        :return: List of available languages.
        """
        process = Environment.run(
            str(self._tesseract_bin),
            "--list-langs",
        )
        # First line is usually 'List of available languages (x):'
        langs: list[str] = []
        for line in process.stdout.splitlines()[1:]:
            line = str(line).strip().lower()
            if not line or line == "none" or line.startswith("list of available"):
                continue
            langs.append(line)
        langs.sort()
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
