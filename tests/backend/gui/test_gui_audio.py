
# tests\backend\gui\test_gui_audio.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.audio import *

from file_conversor.backend.gui.flask_route import FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


class TestGUIAudio:
    def test_index(self):
        url = FlaskRoute.get_url(audio_index)
        Test.flask_webpage(url)

    def test_check(self):
        url = FlaskRoute.get_url(audio_check)
        Test.flask_webpage(url)

    def test_convert(self):
        url = FlaskRoute.get_url(audio_convert)
        Test.flask_webpage(url)

    def test_info(self):
        url = FlaskRoute.get_url(audio_info)
        Test.flask_webpage(url)
