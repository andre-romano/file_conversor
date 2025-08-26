# tests\cli\test_pdf_cmd.py

from pathlib import Path
from tests.utils import Test, DATA_PATH, app_cmd


def test_pdf_help():
    Test.invoke_test_help("pdf")
