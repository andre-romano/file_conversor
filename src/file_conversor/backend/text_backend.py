# src\file_conversor\backend\text_backend.py

from enum import Enum
from pathlib import Path
from typing import Any, Protocol, cast, override

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.config import Configuration, Log
from file_conversor.config.locale import get_translation


# get app config
CONFIG = Configuration.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class TextFileProtocol(Protocol):
    def read(self) -> Any:
        """ Read the data from file. """
        ...

    def write(self, data: Any):
        """ Write the data to file. """
        ...

    def minify(self, data: Any):
        """ Minify the data and write to file. """
        ...


class AbstractTextFile(TextFileProtocol):
    def __init__(self, filename: str | Path) -> None:
        super().__init__()
        self._filepath = Path(filename)


class XMLTextFile(AbstractTextFile):
    @override
    def read(self):
        import xmltodict
        return xmltodict.parse(self._filepath.read_bytes())

    @override
    def write(self, data: Any):
        import xmltodict
        xml_str = xmltodict.unparse(data, pretty=True)
        self._filepath.write_text(xml_str, encoding="utf-8")

    @override
    def minify(self, data: Any):
        import xmltodict
        xml_str = xmltodict.unparse(data, pretty=False)
        self._filepath.write_text(xml_str, encoding="utf-8")


class JSONTextFile(AbstractTextFile):
    @override
    def read(self):
        import json
        return json.loads(self._filepath.read_bytes())

    @override
    def write(self, data: Any):
        import json
        json_str = json.dumps(data, indent=4)
        self._filepath.write_text(json_str, encoding="utf-8")

    @override
    def minify(self, data: Any):
        import json
        json_str = json.dumps(data, separators=(',', ':'), indent=None)
        self._filepath.write_text(json_str, encoding="utf-8")


class YAMLTextFile(AbstractTextFile):
    @override
    def read(self):
        import yaml
        with open(self._filepath, mode="r") as fp:
            return yaml.safe_load(fp)

    @override
    def write(self, data: Any):
        import yaml
        with open(self._filepath, mode="w") as fp:
            yaml.dump(data, fp, indent=2)

    @override
    def minify(self, data: Any):
        import yaml
        with open(self._filepath, mode="w") as fp:
            yaml.dump(
                data,
                fp,
                default_flow_style=True,  # forces inline compact form
                allow_unicode=True,       # preserves UTF-8 chars
            )


class TOMLTextFile(AbstractTextFile):
    @override
    def read(self):
        import toml
        with open(self._filepath, mode="r") as fp:
            return toml.load(fp)

    @override
    def write(self, data: Any):
        import toml
        with open(self._filepath, mode="w") as fp:
            toml.dump(data, fp)

    @override
    def minify(self, data: Any):
        self.write(data)  # toml.dump already writes in compact form


class INITextFile(AbstractTextFile):
    @override
    def read(self):
        import configparser
        config = configparser.ConfigParser()
        config.read(self._filepath)
        return {section: dict(config[section]) for section in config.sections()}

    @override
    def write(self, data: Any):
        import configparser
        if not isinstance(data, dict):
            raise ValueError(f"Cannot convert '{self._filepath}' => INI file. Expected input format: {{section_name: {{key1: value1, key2: value2, ...}} }}.")
        config = configparser.ConfigParser()
        for section, values in cast(dict[Any, Any], data).items():
            if not isinstance(values, dict):
                raise ValueError(f"Cannot convert '{self._filepath}' => INI file. Expected input format: {{section_name: {{key1: value1, key2: value2, ...}} }}")
            values = cast(dict[Any, Any], values)
            config[section] = {str(k): str(v) for k, v in values.items()}
        with open(self._filepath, "w") as f:
            config.write(f)

    @override
    def minify(self, data: Any):
        return self.write(data)  # configparser writes in compact form by default


class TextBackend(AbstractBackend):
    class SupportedInFormats(Enum):
        JSON = "json"
        XML = "xml"
        YAML = "yaml"
        TOML = "toml"
        INI = "ini"

        @property
        def backend(self) -> type[AbstractTextFile]:
            match self:
                case TextBackend.SupportedInFormats.JSON:
                    return JSONTextFile
                case TextBackend.SupportedInFormats.XML:
                    return XMLTextFile
                case TextBackend.SupportedInFormats.YAML:
                    return YAMLTextFile
                case TextBackend.SupportedInFormats.TOML:
                    return TOMLTextFile
                case TextBackend.SupportedInFormats.INI:
                    return INITextFile

    SupportedOutFormats = SupportedInFormats

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

    def convert(
            self,
            input_file: Path,
            output_file: Path,
    ):
        """
        Convert text file to other formats

        :param input_file: Input file
        :param output_file: Output file        
        """
        output_file = output_file.with_suffix(output_file.suffix.lower())

        in_ext = input_file.suffix[1:].lower()
        out_ext = output_file.suffix[1:].lower()

        in_backend = self.SupportedInFormats(in_ext).backend(input_file)
        out_backend = self.SupportedOutFormats(out_ext).backend(output_file)

        data = in_backend.read()
        out_backend.write(data)

    def check(self,
              input_file: Path,
              ):
        """
        Checks if file is wellformed (structure is correct)

        :raises Exception: if file is not well structured
        """
        in_ext = input_file.suffix[1:].lower()
        in_backend = self.SupportedInFormats(in_ext).backend(input_file)

        try:
            in_backend.read()
        except:
            logger.error(rf"'{input_file}': [bold red]FAILED[/]")
            raise
        logger.info(rf"'{input_file}': [bold green]OK[/]")

    def minify(self,
               input_file: Path,
               output_file: Path,
               ):
        """
        Minifies text file

        :param input_file: Input file
        :param output_file: Output file  
        """
        output_file = output_file.with_suffix(output_file.suffix.lower())

        in_ext = input_file.suffix[1:].lower()
        out_ext = output_file.suffix[1:].lower()

        in_backend = self.SupportedInFormats(in_ext).backend(input_file)
        out_backend = self.SupportedOutFormats(out_ext).backend(output_file)

        data = in_backend.read()
        out_backend.minify(data)


__all__ = [
    "TextBackend",
]
