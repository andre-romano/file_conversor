
# tests\backend\gui\test_gui_hash.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.hash import *

from file_conversor.backend.gui.flask_route import FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


class TestGUIHash:
    def test_index(self):
        url = FlaskRoute.get_url(hash_index)
        Test.flask_webpage(url)

    def test_check(self):
        url = FlaskRoute.get_url(hash_check)
        Test.flask_webpage(url)

    def test_create(self):
        url = FlaskRoute.get_url(hash_create)
        Test.flask_webpage(url)
