# src\file_conversor\command\_progress_manager.py


# user-provided
from file_conversor.config.locale import get_translation

_ = get_translation()


class ProgressManager:
    def __init__(self, out_files: int = 1, steps_per_file: int = 1):
        """
        Inits progress manager

        :param out_files: Number of output files
        :param steps_per_file: Number of processing steps per file
        """
        super().__init__()
        if out_files < 1:
            raise ValueError("total_out_files must be >= 1")
        if steps_per_file < 1:
            raise ValueError("total_steps_per_file must be >= 1")

        self._total_out_files = out_files
        self._total_steps_per_file = steps_per_file

        self._completed_files = 0
        self._current_step = 1

    def _next_step(self):
        self._current_step += 1
        if self._current_step > self._total_steps_per_file:
            self._current_step = 1
            self._completed_files += 1

    def get_progress(self, progress: float) -> float:
        """ Get overall progress (0.0 - 100.0) given current step """
        if self._completed_files > self._total_out_files:
            raise RuntimeError(f"ProgressManager - Completed '{self._completed_files}' files > '{self._total_out_files}' total out files")

        file_progress = 100.0 / self._total_out_files
        step_progress = file_progress / self._total_steps_per_file

        # previous completed files
        total_progress = self._completed_files * file_progress

        # previous completed steps (of current file)
        total_progress += (self._current_step - 1) * step_progress

        # current step (of current file)
        total_progress += (progress / 100.0) * step_progress
        return total_progress

    def next_step(self) -> float:
        """ Move to next step and return updated progress """
        progress = self.get_progress(100.0)  # Ensure current step is 100%
        self._next_step()
        return progress


__all__ = [
    "ProgressManager",
]
