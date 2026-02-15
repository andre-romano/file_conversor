
# src\file_conversor\command\pipeline\create_cmd.py

from pathlib import Path
from typing import Any, Callable

# user-provided modules
from file_conversor.backend.batch_backend import BatchBackend
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class PipelineCreateCommand:
    EXTERNAL_DEPENDENCIES = BatchBackend.EXTERNAL_DEPENDENCIES

    @classmethod
    def help(cls):
        return BatchBackend.StageConfigDataModel.help_template()

    @classmethod
    def create(
        cls,
        pipeline_dir: Path,
        stages: list[str],
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        logger.info(f"{_('Creating batch pipeline')} '{pipeline_dir}' ...")

        batch_backend = BatchBackend(pipeline_dir)
        for idx, command in enumerate(stages, start=1):
            batch_backend.pipeline.add_stage(out_dir=f"stage_{idx}", command=command)
            progress_callback(100.0 * float(idx) / len(stages))
        batch_backend.save_config()

        logger.info(f"{_('Pipeline creation')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PipelineCreateCommand",
]
