
# src\file_conversor\cli\pdf\ocr_cmd.py

import typer

from pathlib import Path
from typing import Annotated, Any, Callable, List

from rich import print

# user-provided modules
from file_conversor.backend.pdf import OcrMyPDFBackend

from file_conversor.cli.pdf._typer import TRANSFORMATION_PANEL as RICH_HELP_PANEL
from file_conversor.cli.pdf._typer import COMMAND_NAME, OCR_NAME

from file_conversor.config import Environment, Configuration, State, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils import ProgressManager, CommandManager
from file_conversor.utils.rich_utils import get_progress_bar
from file_conversor.utils.typer_utils import DPIOption, FormatOption, InputFilesArgument, OutputDirOption

from file_conversor.system.win.ctx_menu import WinContextCommand, WinContextMenu

# get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


typer_cmd = typer.Typer()

EXTERNAL_DEPENDENCIES = OcrMyPDFBackend.EXTERNAL_DEPENDENCIES


def register_ctx_menu(ctx_menu: WinContextMenu):
    icons_folder_path = Environment.get_icons_folder()
    for ext in OcrMyPDFBackend.SUPPORTED_IN_FORMATS:
        ctx_menu.add_extension(f".{ext}", [
            WinContextCommand(
                name="ocr",
                description="OCR",
                command=f'cmd.exe /c "{Environment.get_executable()} "{COMMAND_NAME}" "{OCR_NAME}" "%1""',
                icon=str(icons_folder_path / 'ocr.ico'),
            ),
        ])


# register commands in windows context menu
ctx_menu = WinContextMenu.get_instance()
ctx_menu.register_callback(register_ctx_menu)


def execute_pdf_ocr_cmd(
    input_files: List[Path],
    languages: List[str],
    output_dir: Path,
    progress_callback: Callable[[float], Any] = lambda p: p,
):
    ocrmypdf_backend = OcrMyPDFBackend(
        install_deps=CONFIG['install-deps'],
        verbose=STATE['verbose'],
    )
    local_langs: set[str] = ocrmypdf_backend.get_available_languages()
    remote_langs: set[str]

    if 'all' in languages:
        remote_langs = ocrmypdf_backend.get_available_remote_languages()
        print(f"{_('Available remote languages')}: {', '.join(remote_langs)}")
        print(f"{_('Installed languages')}: {', '.join(local_langs)}")
        return

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
                    progress_callback=lambda p, t=task: progress.update(t, completed=p),
                )
                progress.update(task, completed=100)

    for idx, input_file in enumerate(input_files):
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
        progress_callback(100.0 * (float(idx + 1) / len(input_files)))

    logger.info(f"{_('File OCR')}: [green][bold]{_('SUCCESS')}[/bold][/green]")


@typer_cmd.command(
    name=OCR_NAME,
    rich_help_panel=RICH_HELP_PANEL,
    help=f"""
        {_('Create a searchable PDF file from scanned documents using OCR.')}

        {_('Outputs a text searchable PDF file.')}
    """,
    epilog=f"""
        **{_('Examples')}:** 

        - `file_conversor {COMMAND_NAME} {OCR_NAME} input_file.pdf -l all`

        - `file_conversor {COMMAND_NAME} {OCR_NAME} input_file.pdf -l eng`

        - `file_conversor {COMMAND_NAME} {OCR_NAME} input_file.pdf input_file2.pdf -l eng -l por`

        - `file_conversor {COMMAND_NAME} {OCR_NAME} input_file.pdf input_file2.pdf -l eng -od "D:\\Downloads"`
    """)
def ocr(
    input_files: Annotated[List[Path], InputFilesArgument(OcrMyPDFBackend)],

    languages: Annotated[List[str], typer.Option(
        "--languages", "-l",
        help=_("Languages to use for OCR (three character language codes). Format: LANG (e.g., 'eng', 'por'). Type 'all' to query all available languages."),
    )],

    output_dir: Annotated[Path, OutputDirOption()] = Path(),
):
    execute_pdf_ocr_cmd(
        input_files=input_files,
        languages=languages,
        output_dir=output_dir,
    )


__all__ = [
    "typer_cmd",
    "EXTERNAL_DEPENDENCIES",
    "execute_pdf_ocr_cmd",
]
