# tests\cli\test_hash_cmd.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_hash_create_cases(tmp_path):
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


def test_hash_create_help():
    Test.invoke_test_help("hash", "create")
