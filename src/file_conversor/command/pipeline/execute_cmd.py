
# src\file_conversor\command\pipeline\execute_cmd.py

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


class PipelineExecuteCommand:
    EXTERNAL_DEPENDENCIES = BatchBackend.EXTERNAL_DEPENDENCIES

    @classmethod
    def execute(
        cls,
        pipeline_dir: Path,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        logger.info("Executing pipeline ...")
        batch_backend = BatchBackend(pipeline_dir)
        batch_backend.load_config()

        for idx, stage in enumerate(batch_backend.pipeline.stages, start=1):
            stage.execute(lambda p, idx=idx: progress_callback(
                (p + 100.0 * (idx - 1)) / len(batch_backend.pipeline.stages)
                # 0-100 per stage + previous stages completed
            ))

        logger.info(f"{_('Pipeline execution')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PipelineExecuteCommand",
]
