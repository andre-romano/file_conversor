# src\utils\rich.py

from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn


def get_progress_bar() -> Progress:
    """Gets rich Progress() instance, properly formatted"""

    return Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        "[bold white][progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
    )
