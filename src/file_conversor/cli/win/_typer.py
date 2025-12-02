# src\file_conversor\cli\win\_typer.py

# user-provided modules
from file_conversor.config import get_translation

_ = get_translation()

CONTEXT_MENU_PANEL = _("Context menu")
OTHERS_PANEL = _("Other commands")

# command
COMMAND_NAME = "win"

# SUBCOMMANDS
INSTALL_MENU_NAME = "install-menu"
UNINSTALL_MENU_NAME = "uninstall-menu"
RESTART_EXPLORER_NAME = "restart-explorer"

__all__ = [
    "COMMAND_NAME",

    "INSTALL_MENU_NAME",
    "UNINSTALL_MENU_NAME",
    "RESTART_EXPLORER_NAME",
]
