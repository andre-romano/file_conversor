
# tests/test_main.py

import pytest

from typer.testing import CliRunner

from file_conversor import *

runner = CliRunner()

# def test_saudacao():
#     result = runner.invoke(app, ["saudacao", "João"])
#     assert "Olá, João!" in result.output


# def test_saudacao_formal():
#     result = runner.invoke(app, ["saudacao", "Maria", "--formal"])
#     assert "Sr./Sra." in result.output
