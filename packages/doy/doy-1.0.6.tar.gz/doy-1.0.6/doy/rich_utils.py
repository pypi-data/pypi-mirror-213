from typing import *
from rich.progress import *


class RateColumn(ProgressColumn):
    """Renders human readable processing rate."""

    def render(self, task: "Task") -> Text:
        """Render the speed in iterations per second."""
        speed = task.finished_speed or task.speed
        if speed is None:
            return Text("", style="progress.percentage")
        return Text(f"{speed:.2f} it/s", style="progress.percentage")


class TimeElapsedColumn(ProgressColumn):
    """Renders time elapsed."""

    def __init__(
        self, compact: bool = False, table_column: Optional[Column] = None,
    ):
        self.compact = compact
        super().__init__(table_column=table_column)

    def render(self, task: "Task") -> Text:
        """Show time elapsed."""
        elapsed = task.finished_time if task.finished else task.elapsed
        if elapsed is None:
            return Text(
                "--:--" if self.compact else "-:--:--", style="progress.elapsed"
            )

        minutes, seconds = divmod(int(elapsed), 60)
        hours, minutes = divmod(minutes, 60)

        if self.compact and not hours:
            formatted = f"{minutes:02d}:{seconds:02d}"
        else:
            formatted = f"{hours:d}:{minutes:02d}:{seconds:02d}"

        return Text(formatted, style="progress.elapsed")


def track(
    sequence,
    description: str = "Working...",
    total: Optional[float] = None,
    auto_refresh: bool = True,
    console=None,
    transient: bool = False,
    refresh_per_second: float = 12.5,
    update_period: float = 0.1,
    disable: bool = False,
):
    columns = [
        # TaskProgressColumn(show_speed=True),
        # SpinnerColumn('dots10'),
        *(
            [TextColumn("[progress.description]{task.description}")]
            if description
            else []
        ),
        BarColumn(
            bar_width=40,
            style="bar.back",
            complete_style="bar.complete",
            finished_style="bar.finished",
            pulse_style="bar.pulse",
        ),
        MofNCompleteColumn(),
        RateColumn(),
        TimeRemainingColumn(compact=True),
        TimeElapsedColumn(compact=True),
    ]
    progress = Progress(
        *columns,
        auto_refresh=auto_refresh,
        console=console,
        transient=transient,
        refresh_per_second=refresh_per_second or 10,
        disable=disable,
    )

    with progress:
        yield from progress.track(
            sequence, total=total, description=description, update_period=update_period
        )
