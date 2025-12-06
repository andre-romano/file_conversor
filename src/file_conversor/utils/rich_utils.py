# src\file_conversor\utils\rich.py


from types import TracebackType
from typing import Any, Optional, Self, Type

from rich.progress import Progress, TaskID, TextColumn, BarColumn, TimeRemainingColumn

# user-provided
from file_conversor.config.state import State

STATE = State.get_instance()


class DummyProgress(Progress):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def __enter__(self) -> Self:  # type: ignore
        return self

    def __exit__(  # type: ignore
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        pass

    def add_task(self, description: str, start: bool = True, total: float | None = 100, completed: int = 0, visible: bool = True, **fields: Any) -> TaskID:
        return TaskID(0)

    def update(self, task_id: TaskID, *, total: float | None = None, completed: float | None = None, advance: float | None = None, description: str | None = None, visible: bool | None = None, refresh: bool = False, **fields: Any):
        # empty method (does nothing / dummy progress bar)
        pass

    def advance(self, task_id: TaskID, advance: float = 1) -> None:
        # empty method (does nothing / dummy progress bar)
        pass


def get_progress_bar() -> Progress | DummyProgress:
    """Gets rich Progress() instance, properly formatted"""

    if STATE['no-progress']:
        return DummyProgress()
    return Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        "[bold white][progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
    )


__all__ = [
    "get_progress_bar",
]
