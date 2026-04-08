
# src\file_conversor\command\pipeline\create_cmd.py

from pathlib import Path
from typing import override

# user-provided modules
from file_conversor.backend.batch_backend import BatchBackend
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.config import LOG, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)

PipelineCreateExternalDependencies = BatchBackend.EXTERNAL_DEPENDENCIES
PipelineCreateInFormats = BatchBackend.SupportedInFormats
PipelineCreateOutFormats = BatchBackend.SupportedOutFormats


class PipelineCreateCommand(AbstractCommand[PipelineCreateInFormats, PipelineCreateOutFormats]):
    pipeline_dir: Path
    stages: list[str]

    @classmethod
    @override
    def _external_dependencies(cls):
        return PipelineCreateExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return PipelineCreateInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return PipelineCreateOutFormats

    @classmethod
    def help(cls):
        return BatchBackend.StageConfigDataModel.help_template()

    @override
    def execute(self):
        logger.info(f"{_('Creating batch pipeline')} '{self.pipeline_dir}' ...")

        batch_backend = BatchBackend(self.pipeline_dir)
        for idx, command in enumerate(self.stages, start=1):
            batch_backend.pipeline.add_stage(out_dir=f"stage_{idx}", command=command)
            self.progress_callback(100.0 * float(idx) / len(self.stages))
        batch_backend.save_config()

        logger.info(f"{_('Pipeline creation')}: [bold green]{_('SUCCESS')}[/].")


__all__ = [
    "PipelineCreateExternalDependencies",
    "PipelineCreateInFormats",
    "PipelineCreateOutFormats",
    "PipelineCreateCommand",
]
