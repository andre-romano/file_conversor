# tests\cli\test_batch_cmd.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_batch_execute():
    result = Test.invoke("batch", "execute", "--help")
    assert "batch execute" in result.output


def test_batch_create():
    result = Test.invoke("batch", "create", "--help")
    assert "batch create" in result.output


def test_batch():
    result = Test.invoke("batch", "--help")
    assert "batch" in result.output
