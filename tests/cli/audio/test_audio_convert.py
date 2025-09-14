
# tests/cli/audio/test_convert.py

import pytest

from file_conversor.cli.audio._typer import COMMAND_NAME, CONVERT_NAME
from file_conversor.cli.audio.convert_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAudioConvert:
    def test_audio_convert(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.mp3", tmp_path / "test.m4a"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, CONVERT_NAME,
                str(in_path),
                *Test.get_format_params(out_path),
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_audio_convert_help(self,):
        Test.invoke_test_help(COMMAND_NAME, CONVERT_NAME)
