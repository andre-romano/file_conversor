
# tests\backend\gui\test_gui_config.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.config import *

from file_conversor.backend.gui.flask_route import FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


class TestGUIConfig:
    def test_index(self):
        url = FlaskRoute.get_url(config_index)
        Test.flask_webpage(url)
