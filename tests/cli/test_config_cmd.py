# tests\cli\test_batch_cmd.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_config_show():
    result = Test.invoke("config", "show", "--help")
    assert "config show" in result.output


def test_config_set():
    result = Test.invoke("config", "set", "--help")
    assert "config set" in result.output


def test_config():
    result = Test.invoke("config", "--help")
    assert "config" in result.output
