
# src\file_conversor\__main__.py

# user provided imports
from file_conversor.cli import Environment, app_cmd
from file_conversor_core.main import start_app


def _start_app() -> None:
    app_cmd(prog_name=Environment.get_app_name())


# Entry point of the app
def main() -> None:
    start_app(_start_app)


# Start the application
if __name__ == "__main__":
    main()
