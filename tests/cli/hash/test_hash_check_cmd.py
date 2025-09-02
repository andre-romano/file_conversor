# tests\cli\test_hash_cmd.py

import shutil
import pytest

from file_conversor.cli.hash._typer import COMMAND_NAME, CHECK_NAME, CREATE_NAME
from file_conversor.cli.hash.check_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestHashCheck:
    def test_hash_check(self, tmp_path):
        in_paths = [
            DATA_PATH / "test.png",
            DATA_PATH / "test.svg",
        ]
        out_path = tmp_path / f"CHECKSUM.sha512"

        result = Test.invoke(
            COMMAND_NAME, CREATE_NAME,
            *[str(p) for p in in_paths],
            *Test.get_format_params(out_path),
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

        for in_path in in_paths:
            shutil.copy2(src=in_path, dst=tmp_path)

        result = Test.invoke(COMMAND_NAME, CHECK_NAME, str(out_path))
        assert result.exit_code == 0
        assert out_path.exists()

    def test_hash_check_help(self,):
        Test.invoke_test_help(COMMAND_NAME, CHECK_NAME)
