# src\file_conversor\utils\progress_manager.py


# user-provided
from file_conversor.utils.rich_utils import get_progress_bar

from file_conversor.config.locale import get_translation

_ = get_translation()


class ProgressManager:
    def __init__(self, total_out_files: int = 1, total_steps_per_file: int = 1):
        """
        Inits progress manager

        :param total_out_files: Number of output files
        :param total_steps_per_file: Number of processing steps per file
        """
        super().__init__()
        if total_out_files < 1:
            raise ValueError("total_out_files must be >= 1")
        if total_steps_per_file < 1:
            raise ValueError("total_steps_per_file must be >= 1")

        self._progress = get_progress_bar()
        self._total_out_files = total_out_files
        self._total_steps_per_file = total_steps_per_file

        self._completed_files = 0
        self._current_step = 1

        self._file_progress = 100.0 / total_out_files
        self._step_progress = self._file_progress / total_steps_per_file

    @property
    def completed_files(self) -> int:
        return self._completed_files

    @completed_files.setter
    def completed_files(self, value: int):
        if value > self._total_out_files:
            raise RuntimeError("Completed files > Total out files")
        self._completed_files = value

    @property
    def current_step(self) -> int:
        return self._current_step

    @current_step.setter
    def current_step(self, value: int):
        if value > self._total_steps_per_file:
            self.completed_files += 1
            self._current_step = 1
            return
        self._current_step = value

    def __enter__(self):
        self._progress.__enter__()
        self._task = self._progress.add_task(_("Processing files:"), total=100.0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._progress.__exit__(exc_type, exc_val, exc_tb)

    def update_progress(self, step_progress: float) -> float:
        """Update progress for current file"""
        # previous completed files
        total_progress = self._completed_files * self._file_progress
        # previous completed steps (of current file)
        total_progress += (self._current_step - 1) * self._step_progress
        # current step (of current file)
        total_progress += (step_progress / 100.0) * self._step_progress
        self._progress.update(self._task, completed=total_progress)
        return total_progress

    def complete_step(self) -> float:
        """Mark current step as completed and move to next step"""
        progress = self.update_progress(100.0)  # Ensure current step is 100%
        self.current_step += 1
        return progress


__all__ = [
    "ProgressManager",
]
