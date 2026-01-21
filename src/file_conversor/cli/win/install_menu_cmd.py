
# src\file_conversor\cli\win\inst_menu_cmd.py

import typer

from typing import Annotated, Iterable

# user-provided modules

from file_conversor.cli._utils.abstract_typer_command import AbstractTyperCommand

from file_conversor.backend import WinRegBackend

from file_conversor.config import Environment, Configuration, State, Log, get_translation

from file_conversor.system.win import WinContextMenu, restart_explorer

# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WinInstallMenuTyperCommand(AbstractTyperCommand):
    EXTERNAL_DEPENDENCIES = WinRegBackend.EXTERNAL_DEPENDENCIES

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
        winreg_backend = WinRegBackend(verbose=STATE.loglevel.get().is_verbose())

        ctx_menu = WinContextMenu.get_instance(icons_folder=Environment.get_icons_folder())
        reg_file = ctx_menu.get_reg_file()

        logger.info(f"{_('Uninstalling app context menu in Windows Explorer')} ...")
        winreg_backend.delete_keys(reg_file)

        logger.info(f"{_('Installing app context menu in Windows Explorer')} ...")
        winreg_backend.import_file(reg_file)

        if reboot_explorer:
            restart_explorer()
        else:
            logger.warning("Restart explorer.exe or log off from Windows, to make changes effective immediately.")

        logger.info(f"{_('Context Menu Install')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "WinInstallMenuTyperCommand",
]
