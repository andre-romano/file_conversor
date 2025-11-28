
# tests\backend\gui\test_gui_ppt.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.ppt import *
from file_conversor.backend.gui.flask_route import FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


class TestGUIPpt:
    def test_index(self):
        url = FlaskRoute.get_url(ppt_index)
        Test.flask_webpage(url)

    def test_convert(self):
        url = FlaskRoute.get_url(ppt_convert)
        Test.flask_webpage(url)
