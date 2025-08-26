# tests\cli\doc\test__init.py


from tests.utils import Test, DATA_PATH


def test_doc_help():
    Test.invoke_test_help("doc")
