# tests\backend\gui\_api\test_api_config.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.flask_api_status import *

from tests.utils import Test, DATA_PATH, app_cmd


class TestAPIConfig:
    route = "/api/config"

    def test_config(self):
        reply = Test.flask_api(self.route)
        status = Test.flask_api_status(FlaskApiStatus(**reply))
