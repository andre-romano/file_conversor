
# src\file_conversor\cli\win\restart_exp_cmd.py


# user-provided modules
from typing import override

from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.command.win import WinRestartExplorerCommand
from file_conversor.config import Configuration, Log, State, get_translation
from file_conversor.system import WinContextMenu


# get app config
CONFIG = Configuration.get()
LOG = Log.get_instance()
STATE = State.get()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WinRestartExplorerCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES: set[str] = set()

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # No context menu to register

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
            WinRestartExplorerCommand.restart_explorer(task.update)


__all__ = [
    "WinRestartExplorerCLI",
]
