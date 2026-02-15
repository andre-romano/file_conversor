# src\file_conversor\cli\_utils\rich_progress_bar.py

from dataclasses import dataclass
from types import TracebackType
from typing import Optional, Self, Type

import rich.progress

from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn


@dataclass
class RichTask:
    task_obj: rich.progress.Task | None = None
    progress: rich.progress.Progress | None = None

    @property
    def description(self) -> str | None:
        if not self.task_obj:
            return None
        return self.task_obj.description

    @property
    def total(self) -> float | None:
        if not self.task_obj:
            return None
        return self.task_obj.total

    @property
    def visible(self) -> bool:
        if not self.task_obj:
            return False
        return self.task_obj.visible

    @property
    def completed(self) -> float | None:
        if not self.task_obj:
            return None
        return self.task_obj.completed

    @description.setter
    def description(self, value: str) -> None:
        if not self.progress or not self.task_obj:
            return
        self.progress.update(self.task_obj.id, description=value)

    @total.setter
    def total(self, value: float) -> None:
        if not self.progress or not self.task_obj:
            return
        self.progress.update(self.task_obj.id, total=value)

    @completed.setter
    def completed(self, value: float) -> None:
        if not self.progress or not self.task_obj:
            return
        self.progress.update(self.task_obj.id, completed=value)

    @visible.setter
    def visible(self, value: bool) -> None:
        if not self.progress or not self.task_obj:
            return
        self.progress.update(self.task_obj.id, visible=value)

    def update(self, completed: float):
        """ Set the task progress to completed value. """
        if not self.progress or not self.task_obj:
            return
        self.completed = completed

    def stop(self):
        """ Stop the task progress. """
        if not self.progress or not self.task_obj:
            return
        self.progress.stop_task(self.task_obj.id)


class RichProgressBar:
    """ Rich progress bar utils. """

    def __init__(self, progress_enabled: bool) -> None:
        super().__init__()

        self._rich_progress: Progress | None = None
        if progress_enabled:
            self._rich_progress = Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(bar_width=40),
                "[bold white][progress.percentage]{task.percentage:>3.0f}%",
                TimeRemainingColumn(),
            )

    def __enter__(self) -> Self:
        if self._rich_progress:
            self.start()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]):
        if self._rich_progress:
            self.stop()
        return False

    def start(self):
        """ Start the progress bar. """
        if self._rich_progress:
            self._rich_progress.start()

    def stop(self):
        """ Stop the progress bar. """
        if self._rich_progress:
            self._rich_progress.stop()

    def add_task(
        self,
        description: str,
        total: float | None = 100.0,
    ) -> 'RichTask':
        """ 
        Add a task to the progress bar. 

        :param description: Task description
        :param total: Total progress value (Defaults to 100.0). If None, the task will be indeterminate.

        :return: Task object
        """
        if not self._rich_progress:
            return RichTask()
        task_id = self._rich_progress.add_task(description, total=total)
        task = self._rich_progress.tasks[task_id]
        return RichTask(task_obj=task, progress=self._rich_progress)


__all__ = [
    "RichProgressBar",
    "RichTask",
]
