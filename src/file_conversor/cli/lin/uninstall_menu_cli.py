# src/file_conversor/cli/lin/uninstall_menu_cli.py

from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.command.lin import LinUninstallMenuCommand
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


class LinUninstallMenuCLI(AbstractTyperCommand):
    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.uninstall_menu,
            help=f"""
    {_('Uninstalls app context menu (right click in Dolphin file manager).')}
""",
            epilog=f"""
    **{_('Examples')}:**

    - `file_conversor {group_name} {command_name}`
""")

    def uninstall_menu(self):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Uninstalling context menu:"))
            command = LinUninstallMenuCommand(
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "LinUninstallMenuCLI",
]
