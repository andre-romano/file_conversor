
# tests\backend\gui\test_gui_text.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.text import *
from file_conversor.backend.gui.flask_route import FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


class TestGUIText:
    def test_index(self):
        url = FlaskRoute.get_url(text_index)
        Test.flask_webpage(url)

    def test_check(self):
        url = FlaskRoute.get_url(text_check)
        Test.flask_webpage(url)

    def test_compress(self):
        url = FlaskRoute.get_url(text_compress)
        Test.flask_webpage(url)

    def test_convert(self):
        url = FlaskRoute.get_url(text_convert)
        Test.flask_webpage(url)
