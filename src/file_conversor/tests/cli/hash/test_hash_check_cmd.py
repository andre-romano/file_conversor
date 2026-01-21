# tests\cli\test_hash_cmd.py

import shutil
import pytest
from pathlib import Path

from file_conversor.cli._typer import AppCommands, HashTyperGroup
from file_conversor.cli.hash import HashCheckCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(HashCheckCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestHashCheck:
    def test_hash_check(self, tmp_path):
        in_paths: list[Path] = [
            DATA_PATH / "test.png",
            DATA_PATH / "test.svg",
        ]
        out_path = tmp_path / f"CHECKSUM.sha512"

        result = TestTyper.invoke(
            AppCommands.HASH.value, HashTyperGroup.Commands.CREATE.value,
            *[str(p) for p in in_paths],
            *TestTyper.get_format_params(out_path),
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

        for in_path in in_paths:
            shutil.copy2(src=in_path, dst=tmp_path)

        result = TestTyper.invoke(AppCommands.HASH.value, HashTyperGroup.Commands.CHECK.value, str(out_path))
        assert result.exit_code == 0
        assert out_path.exists()

    def test_hash_check_help(self,):
        TestTyper.invoke_test_help(AppCommands.HASH.value, HashTyperGroup.Commands.CHECK.value)
