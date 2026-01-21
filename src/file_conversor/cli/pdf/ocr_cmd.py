
# src\file_conversor\cli\pdf\ocr_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List, Iterable

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, ProgressManagerRich, CommandManagerRich, get_progress_bar
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption

from file_conversor.backend.pdf import OcrMyPDFBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.utils.formatters import get_output_file

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfOcrTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = OcrMyPDFBackend.EXTERNAL_DEPENDENCIES

    def register_ctx_menu(self, ctx_menu: WinContextMenu):
        icons_folder_path = Environment.get_icons_folder()
        for ext in OcrMyPDFBackend.SUPPORTED_IN_FORMATS:
            ctx_menu.add_extension(f".{ext}", [
                WinContextCommand(
                    name="ocr",
                    description="OCR",
                    command=f'cmd.exe /c "{Environment.get_executable()} "{self.GROUP_NAME}" "{self.COMMAND_NAME}" "%1""',
                    icon=str(icons_folder_path / 'ocr.ico'),
                ),
            ])

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.ocr,
            help=f"""
    {_('Create a searchable PDF file from scanned documents using OCR.')}

    {_('Outputs a text searchable PDF file.')}
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name} input_file.pdf -l all`

    - `file_conversor {group_name} {command_name} input_file.pdf -l eng`

    - `file_conversor {group_name} {command_name} input_file.pdf input_file2.pdf -l eng -l por`

    - `file_conversor {group_name} {command_name} input_file.pdf input_file2.pdf -l eng -od "D:\\Downloads"`
""")

    def ocr(
        self,
        input_files: Annotated[List[Path], InputFilesArgument(OcrMyPDFBackend)],

        languages: Annotated[List[str], typer.Option(
            "--languages", "-l",
            help=_("Languages to use for OCR (three character language codes). Format: LANG (e.g., 'eng', 'por'). Type 'all' to query all available languages."),
        )],

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        ocrmypdf_backend = OcrMyPDFBackend(
            install_deps=CONFIG.install_deps,
            verbose=STATE.loglevel.get().is_verbose(),
        )
        languages = [lang.lower() for lang in languages]
        local_langs: set[str] = ocrmypdf_backend.get_available_languages()
        remote_langs: set[str]

        if 'all' in languages:
            remote_langs = ocrmypdf_backend.get_available_remote_languages()
            logger.info(f"{_('Available remote languages')}: {', '.join(remote_langs)}")
            logger.info(f"{_('Installed languages')}: {', '.join(local_langs)}")
            return

        install_langs = set(languages) - local_langs
        if install_langs:
            remote_langs = ocrmypdf_backend.get_available_remote_languages()
            if install_langs - remote_langs:
                logger.info(f"{_('Available remote languages')}: {', '.join(remote_langs)}")
                logger.info(f"{_('Languages requested')}: {', '.join(install_langs)}")
                raise ValueError(f"{_('Some languages are not available for installation')}.")

            with get_progress_bar() as progress:
                for lang in install_langs:
                    task = progress.add_task(f"{_('Installing language')} '{lang}' ...", total=100)
                    ocrmypdf_backend.install_language(
                        lang=lang,
                        progress_callback=lambda p, task=task: progress.update(task, completed=p),
                    )
                    progress.update(task, completed=100)

        for idx, input_file in enumerate(input_files):
            input_file = Path(input_file).resolve()
            output_file = output_dir / get_output_file(input_file, stem="_ocr")
            if not STATE.overwrite_output.enabled and output_file.exists():
                raise FileExistsError(f"{_("File")} '{output_file}' {_("exists")}. {_("Use")} 'file_conversor -oo' {_("to overwrite")}.")

            logger.info(f"Processing '{output_file}' ...")

            ocrmypdf_backend.to_pdf(
                input_file=input_file,
                output_file=output_file,
                languages=languages,
            )
            # progress_callback(100.0 * (float(idx + 1) / len(input_files)))

        logger.info(f"{_('File OCR')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


__all__ = [
    "PdfOcrTyperCommand",
]
