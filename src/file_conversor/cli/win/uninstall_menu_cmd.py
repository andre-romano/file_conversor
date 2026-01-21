
# src\file_conversor\cli\win\unins_cmd.py

from typing import Annotated, Iterable

# user-provided modules
from file_conversor.cli._utils.abstract_typer_command import AbstractTyperCommand

from file_conversor.backend import WinRegBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win.ctx_menu import WinContextMenu

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WinUninstallMenuTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = WinRegBackend.EXTERNAL_DEPENDENCIES

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
        winreg_backend = WinRegBackend(verbose=STATE.loglevel.get().is_verbose())
        ctx_menu = WinContextMenu.get_instance(icons_folder=Environment.get_icons_folder())

        logger.info(f"{_('Removing app context menu from Windows Explorer')} ...")
        winreg_backend.delete_keys(ctx_menu.get_reg_file())

        logger.info(f"{_('Context Menu Uninstall')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "WinUninstallMenuTyperCommand",
]
