# tests\cli\image\test_image_render_cmd.py

import pytest

from file_conversor.cli.image._typer import COMMAND_NAME, RENDER_NAME
from file_conversor.cli.image.render_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestImageRender:
    def test_image_render_cases(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.svg", tmp_path / "test.jpg"),
            (DATA_PATH / "test.svg", tmp_path / "test.png"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, RENDER_NAME,
                str(in_path),
                *Test.get_format_params(out_path),
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_image_render_help(self,):
        Test.invoke_test_help(COMMAND_NAME, RENDER_NAME)
