# tests\cli\test_hash_cmd.py

import pytest

from file_conversor.cli.hash._typer import COMMAND_NAME, CREATE_NAME
from file_conversor.cli.hash.create_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestHashCreate:
    def test_hash_create_cases(self, tmp_path):
        in_paths = [
            DATA_PATH / "test.png",
            DATA_PATH / "test.svg",
        ]
        out_path = tmp_path / f"CHECKSUM.sha256"

        result = Test.invoke(
            COMMAND_NAME, CREATE_NAME,
            *[str(p) for p in in_paths],
            *Test.get_format_params(out_path),
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_hash_create_help(self,):
        Test.invoke_test_help(COMMAND_NAME, CREATE_NAME)
