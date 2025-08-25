# tests\cli\test_pipeline_cmd.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_pipeline_execute():
    result = Test.invoke("pipeline", "execute", "--help")
    assert "pipeline execute" in result.output


def test_pipeline_create():
    result = Test.invoke("pipeline", "create", "--help")
    assert "pipeline create" in result.output


def test_pipeline():
    result = Test.invoke("pipeline", "--help")
    assert "pipeline" in result.output
