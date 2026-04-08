
# src\file_conversor\cli\pdf\ocr_cmd.py

from pathlib import Path
from typing import Annotated, Iterable, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.cli._utils.typer import InputFilesArgument, OutputDirOption
from file_conversor.command.pdf import PdfOcrCommand
from file_conversor.command.pdf.ocr_cmd import PdfOcrLanguageModel
from file_conversor.config import LOG, STATE, get_translation
from file_conversor.system import ContextMenu, ContextMenuItem
from file_conversor.utils.validators import prompt_retry_on_exception


_ = get_translation()
logger = LOG.getLogger(__name__)


class PdfOcrCLI(AbstractTyperCommand):
    @override
    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path):
        for ext_in in PdfOcrCommand.get_in_formats():
            ctx_menu.add_extension(f".{ext_in}", [
                ContextMenuItem(
                    name="ocr",
                    description="OCR",
                    args=[self.GROUP_NAME, self.COMMAND_NAME],
                    icon=icons_folder / 'ocr.ico',
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

    def _print_languages(self, title: str, languages: Iterable[PdfOcrLanguageModel]):
        languages_list = sorted(languages, key=lambda l: l.code)
        logger.info(f"{title}:\n{'\n'.join(
            f"{lang.code} - {lang.name}"
            for lang in languages_list
        )}\n")

    def ocr(
        self,
        input_files: Annotated[list[Path], InputFilesArgument(PdfOcrCommand.get_in_formats())],

        languages: Annotated[list[str] | None, typer.Option(
            "--languages", "-l",
            help=f'{_("Languages to use for OCR (three character language codes, comma-separated) (e.g.,")} "eng", "por"). {_("Type")} "all" {_("to query all available languages.")}',
        )] = None,

        output_dir: Annotated[Path, OutputDirOption()] = Path(),
    ):
        if not languages:
            lang_str = prompt_retry_on_exception(
                f'{_("Languages to use for OCR (three character language codes, comma-separated) (e.g.,")} "eng", "por") [all = {_("query all available languages")}]',
                default="all",
                type=str,
            )
            languages = lang_str.split(",")
        languages = [lang.lower().strip() for lang in languages]

        if 'all' in languages:
            self._print_languages(
                title=f"[bold blue]{_('Available languages')}[/]",
                languages=PdfOcrCommand.get_available_remote_languages(),
            )
            return

        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task_install = progress_bar.add_task(_("Processing files:"))
            command = PdfOcrCommand(
                input_files=input_files,
                languages=languages,
                output_dir=output_dir,
                progress_callback=task_install.update,
            )
            command.execute()


__all__ = [
    "PdfOcrCLI",
]
