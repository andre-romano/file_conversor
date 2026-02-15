
# src\file_conversor\cli\win\inst_menu_cmd.py

from typing import Annotated, override

import typer

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand, RichProgressBar
from file_conversor.command.win import WinInstallMenuCommand
from file_conversor.config import (
    Configuration,
    Log,
    State,
    get_translation,
)
from file_conversor.system import WinContextMenu


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WinInstallMenuCLI(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = WinInstallMenuCommand.EXTERNAL_DEPENDENCIES

    @override
    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        return  # No context menu to register

    def __init__(self, group_name: str, command_name: str, rich_help_panel: str | None) -> None:
        super().__init__(
            rich_help_panel=rich_help_panel,
            group_name=group_name,
            command_name=command_name,
            function=self.install_menu,
            help=f"""
    {_('Installs app context menu (right click in Windows Explorer).')}        
""",
            epilog=f"""
    **{_('Examples')}:** 

    - `file_conversor {group_name} {command_name}` 
""")

    def install_menu(
        self,
        reboot_explorer: Annotated[bool, typer.Option("--restart-explorer", "-re",
                                                      help=_("Restart explorer.exe (to make ctx menu effective immediately). Defaults to False (do not restart, user must log off/in to make ctx menu changes effective)"),
                                                      is_flag=True,
                                                      )] = False,
    ):
        with RichProgressBar(STATE.progress.enabled) as progress_bar:
            task = progress_bar.add_task(_("Installing context menu:"))
            WinInstallMenuCommand.install_menu(
                reboot_explorer=reboot_explorer,
                progress_callback=task.update,
            )


__all__ = [
    "WinInstallMenuCLI",
]
