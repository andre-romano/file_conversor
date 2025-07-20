
# tests/test_main.py

import pytest
import typer

from typer.testing import CliRunner

from file_conversor import app_cmd as app_cmd

runner = CliRunner()


def test_audio_video_convert():
    result = runner.invoke(
        app_cmd, ["audio_video", "convert", "--help"])
    assert "audio_video convert [OPTIONS]" in result.output


def test_audio_video():
    result = runner.invoke(
        app_cmd, ["audio_video", "--help"])
    assert "audio_video [OPTIONS]" in result.output


def test_config_show():
    result = runner.invoke(app_cmd, ["config", "show"])
    assert "Configuration:" in result.output


def test_config_set():
    result = runner.invoke(app_cmd, ["config", "set"])
    assert "Configuration file" in result.output
    assert "updated" in result.output


def test_help_cmd():
    result = runner.invoke(app_cmd, ["help"])
    ctx = typer.Context(typer.main.get_command(app_cmd))
    assert ctx.command.get_help(ctx) in result.output


def test_help_flag():
    result = runner.invoke(app_cmd, ["--help"])
    ctx = typer.Context(typer.main.get_command(app_cmd))
    assert ctx.command.get_help(ctx) in result.output


def test_verbose():
    result = runner.invoke(app_cmd, ["--verbose", "help"])
    assert "Verbose output:" in result.output
    assert "ENABLED" in result.output


# def test_saudacao_formal():
#     result = runner.invoke(app, ["saudacao", "Maria", "--formal"])
#     assert "Sr./Sra." in result.output
