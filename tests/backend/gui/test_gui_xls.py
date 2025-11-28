
# tests\backend\gui\test_gui_xls.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.xls import *
from file_conversor.backend.gui.flask_route import FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


class TestGUIXls:
    def test_index(self):
        url = FlaskRoute.get_url(xls_index)
        Test.flask_webpage(url)

    def test_convert(self):
        url = FlaskRoute.get_url(xls_convert)
        Test.flask_webpage(url)
