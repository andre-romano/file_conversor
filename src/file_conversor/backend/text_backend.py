# src\file_conversor\backend\text_backend.py

import toml
import json
import yaml
import xmltodict
import configparser

from typing import Any, Callable, Iterable, Sequence

from pathlib import Path

from rich import print

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend

from file_conversor.config import Environment, Configuration, Log
from file_conversor.config.locale import get_translation

# get app config
CONFIG = Configuration.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class AbstractTextFile:
    def __init__(self, filename: str | Path) -> None:
        super().__init__()
        self._filepath = Path(filename)

    def read(self) -> Any:
        raise NotImplementedError("not implemented")

    def write(self, data: Any):
        raise NotImplementedError("not implemented")

    def minify(self, data: Any):
        self.write(data)


class XMLTextFile(AbstractTextFile):
    def read(self):
        return xmltodict.parse(self._filepath.read_bytes())

    def write(self, data: Any, **kwargs):
        xml_str = xmltodict.unparse(data, pretty=True)
        self._filepath.write_text(xml_str, encoding="utf-8")

    def minify(self, data: Any):
        xml_str = xmltodict.unparse(data, pretty=False)
        self._filepath.write_text(xml_str, encoding="utf-8")


class JSONTextFile(AbstractTextFile):
    def read(self):
        return json.loads(self._filepath.read_bytes())

    def write(self, data: Any):
        json_str = json.dumps(data, indent=4)
        self._filepath.write_text(json_str, encoding="utf-8")

    def minify(self, data: Any):
        json_str = json.dumps(data, separators=(',', ':'), indent=None)
        self._filepath.write_text(json_str, encoding="utf-8")


class YAMLTextFile(AbstractTextFile):
    def read(self):
        with open(self._filepath, mode="r") as fp:
            return yaml.safe_load(fp)

    def write(self, data: Any):
        with open(self._filepath, mode="w") as fp:
            yaml.dump(data, fp, indent=2)

    def minify(self, data: Any):
        with open(self._filepath, mode="w") as fp:
            yaml.dump(
                data,
                fp,
                default_flow_style=True,  # forces inline compact form
                allow_unicode=True,       # preserves UTF-8 chars
            )


class TOMLTextFile(AbstractTextFile):
    def read(self):
        with open(self._filepath, mode="r") as fp:
            return toml.load(fp)

    def write(self, data: Any):
        with open(self._filepath, mode="w") as fp:
            toml.dump(data, fp)


class INITextFile(AbstractTextFile):
    def read(self):
        config = configparser.ConfigParser()
        config.read(self._filepath)
        return {section: dict(config[section]) for section in config.sections()}

    def write(self, data: Any):
        if not isinstance(data, dict):
            raise ValueError(f"Cannot convert '{self._filepath}' => INI file. Expected input format: {{section_name: {{key1: value1, key2: value2, ...}} }}.")
        config = configparser.ConfigParser()
        for section, values in data.items():
            if not isinstance(values, dict):
                raise ValueError(f"Cannot convert '{self._filepath}' => INI file. Expected input format: {{section_name: {{key1: value1, key2: value2, ...}} }}")
            config[section] = {str(k): str(v) for k, v in values.items()}
        with open(self._filepath, "w") as f:
            config.write(f)


class TextBackend(AbstractBackend):
    SUPPORTED_IN_FORMATS = {
        "json": {
            "cls": JSONTextFile,
        },
        "xml": {
            "cls": XMLTextFile,
        },
        "yaml": {
            "cls": YAMLTextFile,
        },
        "toml": {
            "cls": TOMLTextFile,
        },
        "ini": {
            "cls": INITextFile,
        },
    }
    SUPPORTED_OUT_FORMATS = {
        "json": {
            "cls": JSONTextFile,
        },
        "xml": {
            "cls": XMLTextFile,
        },
        "yaml": {
            "cls": YAMLTextFile,
        },
        "toml": {
            "cls": TOMLTextFile,
        },
        "ini": {
            "cls": INITextFile,
        },
    }
    EXTERNAL_DEPENDENCIES: set[str] = set()

    def __init__(
        self,
        verbose: bool = False,
    ):
        """
        Initialize the Batch backend.
        """
        super().__init__()
        self._verbose = verbose

    def _get_text_file(
            self,
            filepath: Path,
            formats: dict[str, dict[str, type]],
    ) -> tuple[str, AbstractTextFile]:
        """"Checks file format and returns (ext, textfile)"""
        ext = filepath.suffix[1:]
        if ext not in formats:
            raise ValueError(f"Unsupported input format '{ext}'. Supported formats: {', '.join(formats)}")
        if "cls" not in formats[ext]:
            raise ValueError(f"Cannot find class for format '{ext}'.")
        cls = formats[ext]["cls"]
        text_file = cls(filepath)
        # logger.debug(f"Filepath: {filepath} - Class: {type(text_file)}")
        return (ext, text_file)

    def convert(
            self,
            input_file: str | Path,
            output_file: str | Path,
    ):
        """
        Convert text file to other formats

        :param input_file: Input file
        :param output_file: Output file        
        """
        input_file = Path(input_file)
        output_file = Path(output_file)
        output_file = output_file.with_suffix(output_file.suffix.lower())

        _, in_txt_file = self._get_text_file(input_file, self.SUPPORTED_IN_FORMATS)
        _, out_txt_file = self._get_text_file(output_file, self.SUPPORTED_OUT_FORMATS)

        data = in_txt_file.read()
        out_txt_file.write(data)

    def check(self,
              input_file: str | Path,
              ):
        """
        Checks if file is wellformed (structure is correct)

        :raises Exception: if file is not well structured
        """
        input_file = Path(input_file)

        _, in_txt_file = self._get_text_file(input_file, self.SUPPORTED_IN_FORMATS)
        try:
            in_txt_file.read()
        except:
            logger.error(rf"'{input_file}': [bold red]FAILED[/]")
            raise
        logger.info(rf"'{input_file}': [bold green]OK[/]")

    def minify(self,
               input_file: str | Path,
               output_file: str | Path,
               ):
        """
        Minifies text file

        :param input_file: Input file
        :param output_file: Output file  
        """
        input_file = Path(input_file)
        output_file = Path(output_file)
        output_file = output_file.with_suffix(output_file.suffix.lower())

        _, in_txt_file = self._get_text_file(input_file, self.SUPPORTED_IN_FORMATS)
        _, out_txt_file = self._get_text_file(output_file, self.SUPPORTED_OUT_FORMATS)

        data = in_txt_file.read()
        out_txt_file.minify(data)


__all__ = [
    "TextBackend",
]
