
# src\file_conversor\cli\win\unins_cmd.py


# user-provided modules
from typing import override

from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.command.win import WinUninstallMenuCommand
from file_conversor.config import (
    Configuration,
    Log,
    State,
    get_translation,
)
from file_conversor.system.win.ctx_menu import WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WinUninstallMenuCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = WinUninstallMenuCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # No context menu to register

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.uninstall_menu,
            help=f"""
    {_('Uninstalls app context menu (right click in Windows Explorer).')}        
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name}` 
""")

    def uninstall_menu(self):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Uninstalling context menu:"))
            WinUninstallMenuCommand.uninstall_menu(
                progress_callback=task.update,
            )


__all__ = [
    "WinUninstallMenuCLI",
]
