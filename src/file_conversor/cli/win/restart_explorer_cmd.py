
# src\file_conversor\cli\win\restart_exp_cmd.py

from typing import Annotated, Iterable

# user-provided modules
from file_conversor.cli._utils import AbstractTyperCommand

from file_conversor.config import Configuration, Log, get_translation

from file_conversor.system import WinContextMenu, WindowsSystem, System

# get app config
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WinRestartExplorerTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = set()

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
        if isinstance(System, WindowsSystem):
            logger.info(f"{_('Restarting explorer.exe')} ...")
            System.restart_explorer()


__all__ = [
    "WinRestartExplorerTyperCommand",
]
