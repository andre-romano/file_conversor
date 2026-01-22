# tests\cli\test_hash_cmd.py

import pytest
from pathlib import Path

from file_conversor.cli import AppTyperGroup, HashTyperGroup
from file_conversor.cli.hash import HashCreateCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(HashCreateCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestHashCreate:
    def test_hash_create_cases(self, tmp_path):
        in_paths: list[Path] = [
            DATA_PATH / "test.png",
            DATA_PATH / "test.svg",
        ]
        out_path = tmp_path / f"CHECKSUM.sha256"

        result = TestTyper.invoke(
            AppTyperGroup.Commands.HASH.value, HashTyperGroup.Commands.CREATE.value,
            *[str(p) for p in in_paths],
            *TestTyper.get_format_params(out_path),
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

    def test_hash_create_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.HASH.value, HashTyperGroup.Commands.CREATE.value)
