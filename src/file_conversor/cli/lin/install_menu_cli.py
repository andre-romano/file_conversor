# src/file_conversor/cli/lin/install_menu_cli.py

from typing import Annotated

import typer

from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.command.lin import LinInstallMenuCommand
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


class LinInstallMenuCLI(AbstractTyperCommand):
    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.install_menu,
            help=f"""
    {_('Installs app context menu (right click in Dolphin file manager).')}
""",
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name}`
""")

    def install_menu(
        self,
        rebuild_cache: Annotated[bool, typer.Option(
            "--rebuild-cache", "-rc",
            help=_("Rebuild KDE service cache after install (to make context menu effective immediately). Defaults to False."),
            is_flag=True,
        )] = False,
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Installing context menu:"))
            command = LinInstallMenuCommand(
                rebuild_cache=rebuild_cache,
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "LinInstallMenuCLI",
]
