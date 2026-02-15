# tests\cli\hash\test_hash_check_cli.py

import shutil

from pathlib import Path

import pytest

from file_conversor.cli import AppTyperGroup, HashTyperGroup
from file_conversor.cli.hash import HashCheckCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(HashCheckCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestHashCheckCLI:
    def test_hash_check(self, tmp_path: Path):
        in_paths: list[Path] = [
            DATA_PATH / "test.png",
            DATA_PATH / "test.svg",
        ]
        out_path = tmp_path / f"CHECKSUM.sha512"

        result = TestTyper.invoke(
            AppTyperGroup.Commands.HASH.value, HashTyperGroup.Commands.CREATE.value,
            *[str(p) for p in in_paths],
            *TestTyper.get_format_params(out_path),
            *TestTyper.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()

        for in_path in in_paths:
            shutil.copy2(src=in_path, dst=tmp_path)

        result = TestTyper.invoke(AppTyperGroup.Commands.HASH.value, HashTyperGroup.Commands.CHECK.value, str(out_path))
        assert result.exit_code == 0
        assert out_path.exists()

    def test_hash_check_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.HASH.value, HashTyperGroup.Commands.CHECK.value)
