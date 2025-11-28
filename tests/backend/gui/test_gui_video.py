
# tests\backend\gui\test_gui_video.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.video import *
from file_conversor.backend.gui.flask_route import FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


class TestGUIVideo:
    def test_index(self):
        url = FlaskRoute.get_url(video_index)
        Test.flask_webpage(url)

    def test_check(self):
        url = FlaskRoute.get_url(video_check)
        Test.flask_webpage(url)

    def test_compress(self):
        url = FlaskRoute.get_url(video_compress)
        Test.flask_webpage(url)

    def test_convert(self):
        url = FlaskRoute.get_url(video_convert)
        Test.flask_webpage(url)

    def test_enhance(self):
        url = FlaskRoute.get_url(video_enhance)
        Test.flask_webpage(url)

    def test_info(self):
        url = FlaskRoute.get_url(video_info)
        Test.flask_webpage(url)

    def test_mirror(self):
        url = FlaskRoute.get_url(video_mirror)
        Test.flask_webpage(url)

    def test_resize(self):
        url = FlaskRoute.get_url(video_resize)
        Test.flask_webpage(url)

    def test_rotate(self):
        url = FlaskRoute.get_url(video_rotate)
        Test.flask_webpage(url)
