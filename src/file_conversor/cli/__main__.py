
# src\file_conversor\cli\__main__.py

# user provided imports
from file_conversor.cli import AppTyperGroup
from file_conversor.main_helper import MainHelper


# Entry point of the app
def main() -> None:
    """ Main entry point for the CLI application. """
    def _start_cli() -> int:
        """ Starts the CLI application. """
        cli_app = AppTyperGroup()
        cli_app.run()
        return 0

    main_helper = MainHelper()
    main_helper.run(_start_cli)


# Start the application
if __name__ == "__main__":
    main()
