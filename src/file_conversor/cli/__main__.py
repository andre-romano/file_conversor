
# src\file_conversor\cli\__main__.py

# user provided imports
from file_conversor.cli import AppTyperGroup, Log, State, get_translation
from file_conversor.main_helper import MainHelper


LOG = Log.get_instance()
STATE = State.get()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _start_cli() -> int:
    """ Starts the CLI application. """
    try:
        cli_app = AppTyperGroup()
        cli_app.run()
        return 0
    except Exception as e:
        import subprocess

        debug_mode = STATE.loglevel.level.is_debug()
        error_type = str(type(e))
        error_type = error_type.split("'")[1]
        logger.error(f"{error_type} ({e})", exc_info=True if debug_mode else None)

        if isinstance(e, subprocess.CalledProcessError):
            logger.error(f"CMD: {e.cmd} ({e.returncode})")
            logger.error(f"STDERR: {e.stderr}")
            logger.error(f"STDOUT: {e.stdout}")

        if debug_mode:
            raise
        return 1

# Entry point of the app


def main() -> None:
    """ Main entry point for the CLI application. """
    main_helper = MainHelper()
    main_helper.run(_start_cli)


# Start the application
if __name__ == "__main__":
    main()
