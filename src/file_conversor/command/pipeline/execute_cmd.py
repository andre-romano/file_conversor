
# src\file_conversor\command\pipeline\execute_cmd.py

from pathlib import Path
from typing import override

# user-provided modules
from file_conversor.backend.batch_backend import BatchBackend
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.config import LOG, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


PipelineExecuteExternalDependencies = BatchBackend.EXTERNAL_DEPENDENCIES
PipelineExecuteInFormats = BatchBackend.SupportedInFormats
PipelineExecuteOutFormats = BatchBackend.SupportedOutFormats


class PipelineExecuteCommand(AbstractCommand[PipelineExecuteInFormats, PipelineExecuteOutFormats]):
    pipeline_dir: Path

    @classmethod
    @override
    def _external_dependencies(cls):
        return PipelineExecuteExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PipelineExecuteInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PipelineExecuteOutFormats

    @override
    def execute(self):
        logger.info("Executing pipeline ...")
        batch_backend = BatchBackend(self.pipeline_dir)
        batch_backend.load_config()

        for idx, stage in enumerate(batch_backend.pipeline.stages, start=1):
            stage.execute(lambda p, idx=idx: self.progress_callback(
                (p + 100.0 * (idx - 1)) / len(batch_backend.pipeline.stages)
                # 0-100 per stage + previous stages completed
            ))

        logger.info(f"{_('Pipeline execution')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PipelineExecuteExternalDependencies",
    "PipelineExecuteInFormats",
    "PipelineExecuteOutFormats",
    "PipelineExecuteCommand",
]
