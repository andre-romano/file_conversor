# tests\utils\test_formatters.py


import pytest

from file_conversor.utils.formatters import (
    escape_xml,
    format_alphanumeric,
    format_bitrate,
    format_bytes,
    format_file_types_webview,
    format_py_to_js,
    format_traceback_html,
    format_traceback_str,
    normalize_degree,
    parse_bytes,
    parse_ffmpeg_filter,
    parse_js_to_py,
    parse_pdf_pages,
    parse_pdf_rotation,
    parse_traceback_list,
)


class TestUtilsFormatters:
    def test_escape_xml(self):
        assert escape_xml(None) == ""
        assert escape_xml("Test & <XML> 'Formatter' \"Function\"") == "Test &amp; &lt;XML&gt; &apos;Formatter&apos; &quot;Function&quot;"
        assert escape_xml(123) == "123"

    def test_parse_traceback_list(self):
        try:
            1 / 0  # type: ignore  # noqa: B018
        except Exception as e:
            tb_list = parse_traceback_list(e)
            assert isinstance(tb_list, list)
            assert any("ZeroDivisionError" in line for line in tb_list)

    def test_parse_js_to_py(self):
        assert parse_js_to_py("true") is True
        assert parse_js_to_py("on") is True
        assert parse_js_to_py("false") is False
        assert parse_js_to_py("off") is False
        assert parse_js_to_py("none") is None
        assert parse_js_to_py("null") is None
        assert parse_js_to_py("undefined") is None
        assert parse_js_to_py("42") == 42
        assert parse_js_to_py("-3.14") == -3.14
        assert parse_js_to_py("-3,14") == -3.14
        assert parse_js_to_py("some string") == "some string"
        assert parse_js_to_py("[1, 2, 3]") == [1, 2, 3]
        assert parse_js_to_py('{"key": "value"}') == {"key": "value"}

        with pytest.raises(Exception):  # noqa: B017, B018
            parse_js_to_py("{invalid: }")

    def test_parse_ffmpeg_filter(self):
        name, args_list, args_dict = parse_ffmpeg_filter("")
        assert name == ""
        assert args_list == []
        assert args_dict == {}

        filter_str = "scale=1280:720"
        name, args_list, args_dict = parse_ffmpeg_filter(filter_str)
        assert name == "scale"
        assert args_list == ["1280", "720"]
        assert args_dict == {}

        filter_str = "crop=iw/2:ih/2:0:0"
        name, args_list, args_dict = parse_ffmpeg_filter(filter_str)
        assert name == "crop"
        assert args_list == ["iw/2", "ih/2", "0", "0"]
        assert args_dict == {}

        filter_str = "drawtext=text='Sample Text':fontcolor=white:fontsize=24:x=10:y=10"
        name, args_list, args_dict = parse_ffmpeg_filter(filter_str)
        assert name == "drawtext"
        assert args_list == []
        assert args_dict == {
            "text": "'Sample Text'",
            "fontcolor": "white",
            "fontsize": "24",
            "x": "10",
            "y": "10"
        }

    def test_parse_pdf_rotation(self):
        rotation_args = ["1:90", "2-4:-90", "5:180"]
        rotation_dict = parse_pdf_rotation(rotation_args, last_page=5)
        assert rotation_dict == {
            0: 90,
            1: -90,
            2: -90,
            3: -90,
            4: 180
        }

        rotation_args = ["1-:90"]
        rotation_dict = parse_pdf_rotation(rotation_args, last_page=3)
        assert rotation_dict == {
            0: 90,
            1: 90,
            2: 90
        }

        with pytest.raises(RuntimeError):
            parse_pdf_rotation(["3-1:90"], last_page=5)

    def test_parse_pdf_pages(self):
        pages = parse_pdf_pages(["2", "4", "6"])
        assert pages == [1, 3, 5]

        pages = parse_pdf_pages(["2-4", "6"])
        assert pages == [1, 2, 3, 5]

        with pytest.raises(RuntimeError):
            parse_pdf_pages(["4-2"])

        pages = parse_pdf_pages(["3-"])
        assert pages == [2]  # Assuming last_page is not needed here

    def test_normalize_degree(self):
        assert normalize_degree(450) == 90
        assert normalize_degree(-90) == 270
        assert normalize_degree(720) == 0
        assert normalize_degree(0) == 0
        assert normalize_degree(360) == 0
        assert normalize_degree(355.75) == 355

    def test_parse_bytes(self):
        assert parse_bytes("1024") == 1024
        assert parse_bytes("1 K") == 1024
        assert parse_bytes("1 M") == 1024 * 1024
        assert parse_bytes("1.5 G") == int(1.5 * 1024 * 1024 * 1024)
        assert parse_bytes("2.5 T") == int(2.5 * 1024 * 1024 * 1024 * 1024)

        with pytest.raises(ValueError):
            parse_bytes("2 P")

        with pytest.raises(ValueError):
            parse_bytes("invalid size")

    def test_format_bytes(self):
        assert format_bytes(500) == "500.0 B"
        assert format_bytes(2048) == "2.0 KB"
        assert format_bytes(5 * 1024 * 1024) == "5.0 MB"
        assert format_bytes(3 * 1024 * 1024 * 1024) == "3.0 GB"
        assert format_bytes(7 * 1024 * 1024 * 1024 * 1024) == "7.0 TB"

    def test_format_bitrate(self):
        assert format_bitrate(500) == "500 bps"
        assert format_bitrate(2048) == "2.0 Kbps"
        assert format_bitrate(5 * 1024 * 1024) == "5.0 Mbps"
        assert format_bitrate(3 * 1024 * 1024 * 1024) == "3.0 Gbps"
        assert format_bitrate(4 * 1024 * 1024 * 1024 * 1024) == "4.0 Tbps"

    def test_format_alphanumeric(self):
        assert format_alphanumeric("normal_filename") == "normal_filename"
        assert format_alphanumeric("file@name#1!") == "filename1"
        assert format_alphanumeric("áxís") == "axis"
        assert format_alphanumeric("café résûmé") == "cafe resume"
        assert format_alphanumeric("  spaced \t\n  name   ") == "spaced name"
        assert format_alphanumeric("naïve façade jalapeño") == "naive facade jalapeno"

    def test_format_file_types_webview(self):
        assert format_file_types_webview().endswith("(*.*)")
        assert format_file_types_webview("*.mp4", "*.avi").endswith("(*.mp4;*.avi)")
        assert format_file_types_webview("pdf", description="PDF files") == "PDF files (*.pdf)"
        assert format_file_types_webview("jpg", "png", "gif", description="Image files") == "Image files (*.jpg;*.png;*.gif)"
        assert format_file_types_webview(".jpg", ".png", ".gif", description="Image files") == "Image files (*.jpg;*.png;*.gif)"
        assert format_file_types_webview("*.jpg", "*.png", "*.gif", description="Image files") == "Image files (*.jpg;*.png;*.gif)"

    def test_format_py_to_js(self):
        assert format_py_to_js(True) == "true"
        assert format_py_to_js(False) == "false"
        assert format_py_to_js(None) == "null"
        assert format_py_to_js(42) == "42"
        assert format_py_to_js(-3.14) == "-3.14"
        assert format_py_to_js("some string") == '`some string`'
        assert format_py_to_js("") == '``'
        assert format_py_to_js({"key": "value"}) == '{"key": "value"}'
        assert format_py_to_js([1, 2, 3]) == "[1, 2, 3]"
        assert format_py_to_js((1, 2)) == "[1, 2]"

    def test_format_traceback_str(self):
        try:
            1 / 0  # type: ignore  # noqa: B018
        except Exception as e:
            tb_str = format_traceback_str(e)
            assert "ZeroDivisionError" in tb_str

    def test_format_traceback_html(self):
        try:
            1 / 0  # type: ignore  # noqa: B018
        except Exception as e:
            tb_html = format_traceback_html(e)
            assert "ZeroDivisionError" in tb_html
            assert "&lt;traceback&gt;" not in tb_html  # Ensure HTML is properly formatted
