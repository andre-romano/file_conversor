# src\file_conversor\cli\win\__init__.py

import typer

# user-provided modules
from file_conversor.cli.win.install_menu_cmd import typer_cmd as install_menu_cmd
from file_conversor.cli.win.restart_explorer_cmd import typer_cmd as restart_explorer_cmd
from file_conversor.cli.win.uninstall_menu_cmd import typer_cmd as uninstall_menu_cmd

win_cmd = typer.Typer()
win_cmd.add_typer(restart_explorer_cmd)

# CONTEXT_MENU_PANEL
win_cmd.add_typer(install_menu_cmd)
win_cmd.add_typer(uninstall_menu_cmd)
