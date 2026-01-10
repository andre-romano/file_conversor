
# src\file_conversor_gui\__main__.py

import subprocess
import sys

# user provided imports
from file_conversor.config import get_translation

from file_conversor_core.main import start_app

_ = get_translation()


# Entry point of the app
def main() -> None:
    def callback() -> None:
        print(_("Starting GUI application ..."))
    start_app(callback)


# Start the application
if __name__ == "__main__":
    main()
