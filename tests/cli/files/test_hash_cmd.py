# tests\cli\test_hash_cmd.py

import shutil
from tests.utils import Test, DATA_PATH, app_cmd


def test_hash_check(tmp_path):
    in_paths = [
        DATA_PATH / "test.png",
        DATA_PATH / "test.svg",
    ]
    out_path = tmp_path / f"CHECKSUM.sha512"

    result = Test.invoke(
        "hash", "create",
        *[str(p) for p in in_paths],
        *Test.get_format_params(out_path),
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()

    for in_path in in_paths:
        shutil.copy2(src=in_path, dst=tmp_path)

    result = Test.invoke("hash", "check", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()


def test_hash_create(tmp_path):
    in_paths = [
        DATA_PATH / "test.png",
        DATA_PATH / "test.svg",
    ]
    out_path = tmp_path / f"CHECKSUM.sha256"

    result = Test.invoke(
        "hash", "create",
        *[str(p) for p in in_paths],
        *Test.get_format_params(out_path),
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_hash():
    result = Test.invoke("hash", "--help")
    assert "hash" in result.output
