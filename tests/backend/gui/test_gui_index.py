
# tests\backend\gui\test_gui_index.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.index import index
from file_conversor.backend.gui.flask_route import FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


class TestGUIIndex:
    def test_index(self):
        url = FlaskRoute.get_url(index)
        Test.flask_webpage(url)
