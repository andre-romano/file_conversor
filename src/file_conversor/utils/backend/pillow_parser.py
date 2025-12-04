# src/file_conversor/utils/backend/pillow_parser.py

from pathlib import Path
from typing import Any

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.console import Group

# user-provided imports
from file_conversor.backend.image import PillowBackend

from file_conversor.utils.dominate_utils import br, div

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


class _PillowExifInfo:
    def __init__(self, input_file: Path, metadata: PillowBackend.Exif) -> None:
        super().__init__()
        self.input_file = input_file
        self.metadata = metadata

    def _parse(self):
        input_name = self.input_file.name
        in_ext = self.input_file.suffix.upper()[1:]
        return (input_name, in_ext)

    def rich(self):
        input_name, in_ext = self._parse()
        formatted = [
            f"{_('File Information')}:",
            f"  - {_('Name')}: {input_name}",
            f"  - {_('Format')}: {in_ext}",
        ]
        for tag, value in self.metadata.items():
            tag_name = PillowBackend.Exif_TAGS.get(tag, f"{tag}")
            formatted.append(f"  - {tag_name}: {value}")
        return formatted

    def div(self):
        input_name, in_ext = self._parse()
        with div() as result:
            div(f"{_('File Information')}:")
            div(f"  - {_('Name')}: {input_name}")
            div(f"  - {_('Format')}: {in_ext}")
            for tag, value in self.metadata.items():
                tag_name = PillowBackend.Exif_TAGS.get(tag, f"{tag}")
                div(f"  - {tag_name}: {value}")
            br()
        return result


class PillowParser:
    EXTERNAL_DEPENDENCIES = PillowBackend.EXTERNAL_DEPENDENCIES

    def __init__(self, backend: PillowBackend, input_file: Path) -> None:
        super().__init__()
        self.input_file = input_file
        self.backend = backend

    def run(self):
        try:
            self.metadata = self.backend.info(self.input_file)
        except Exception as e:
            raise RuntimeError(f"{_('File')} '{self.input_file}' {_('is corrupted or has inconsistencies')} - {repr(e)}")

    def get_exif_info(self):
        return _PillowExifInfo(self.input_file, self.metadata)


__all__ = [
    "PillowParser",
]
