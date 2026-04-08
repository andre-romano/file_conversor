
# src\file_conversor\cli\win\restart_exp_cmd.py


# user-provided modules

from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.command.win import WinRestartExplorerCommand
from file_conversor.config import LOG, STATE, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


class WinRestartExplorerCLI(AbstractTyperCommand):
    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.restart_explorer,
            help=f"""
    {_('Restarts explorer.exe (to refresh ctx menus).')}        
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name}` 
""")

    def restart_explorer(self):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Restarting explorer.exe:"))
            command = WinRestartExplorerCommand(
                progress_callback=task.update,
            )
            command.execute()


__all__ = [
    "WinRestartExplorerCLI",
]
