
# src\file_conversor\cli\__main__.py

# user provided imports
from file_conversor.cli import Environment, app_cmd
from file_conversor.main_helper import main_helper


def _start_cli() -> None:
    """ Starts the CLI application. """
    app_cmd(prog_name=Environment.get_app_name())


# Entry point of the app
def main() -> None:
    """ Main entry point for the CLI application. """
    main_helper(_start_cli)


# Start the application
if __name__ == "__main__":
    main()
