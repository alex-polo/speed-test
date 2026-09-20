from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.prompt import Prompt
from rich.table import Table

COLOR_PRIMARY = "blue"
COLOR_SUCCESS = "bright_green"
COLOR_ERROR = "bright_red"
COLOR_DIM = "dim"


class UIClient:
    """UI client for the speed test."""

    def __init__(
        self,
        total_iterations: int,
        bytes_in_mb: int,
    ) -> None:
        """Initializes the UI client."""
        self.total_iterations = total_iterations
        self.bytes_in_mb = bytes_in_mb
        self.console = Console()
        self.fmt_split_line = f"[{COLOR_DIM}]{'─' * 100}[/{COLOR_DIM}]"

    def progress(self, iteration: int) -> Progress:
        """Creates a sleek progress bar."""
        return Progress(
            TextColumn(
                f"[bold {COLOR_PRIMARY}]Request {iteration}/{self.total_iterations}[/]"
            ),
            BarColumn(
                bar_width=40,
                style=f"dim {COLOR_PRIMARY}",
                complete_style=COLOR_PRIMARY,
                finished_style=f"bold {COLOR_SUCCESS}",
            ),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=self.console,
        )

    def ask_url(self) -> str:
        """Asks user for url."""
        self.console.print(
            f"[{COLOR_DIM}]Enter the URL of the file to test:[/{COLOR_DIM}]"
        )
        url = Prompt.ask(f"\t[{COLOR_PRIMARY}]URL[/]")
        self.console.print(self.fmt_split_line)
        return url.strip()

    def print_error(self, msg: str) -> None:
        """Prints error message."""
        self.console.print(f"\n[bold {COLOR_ERROR}]❌ Error:[/] {msg}\n")

    def print_starting_header(self) -> None:
        """Prints starting header."""
        self.console.print(f"\n{self.fmt_split_line}")
        self.console.print(
            " [bold]NETWORK SPEED TEST[/]", style=f"bold {COLOR_PRIMARY}"
        )
        self.console.print(self.fmt_split_line + "\n")

    def print_speed_test_params(self, url: str, file_size: int) -> None:
        """Prints speed test params with clear label/value hierarchy."""
        self.console.print(f"\t[{COLOR_DIM}]Target URL:[/]\t[bold]{url}[/]")
        self.console.print(
            f"\t[{COLOR_DIM}]File size:[/]\t[bold]{(file_size / self.bytes_in_mb):.2f} MB[/]"  # ruff: ignore[line-too-long]
        )
        self.console.print(
            f"\t[{COLOR_DIM}]Iterations:[/]\t[bold]{self.total_iterations}[/]"
        )
        self.console.print(f"{self.fmt_split_line}\n")

    def print_info_downloaded(self, req_time: float, req_bytes: int) -> None:
        """Prints info about downloaded request."""
        self.console.print(
            f"\t\t[{COLOR_SUCCESS}][REQ][/] "
            f"[{COLOR_DIM}]Time:[/] {req_time:.3f} sec  "
            f"[{COLOR_DIM}]Size:[/] {req_bytes / self.bytes_in_mb:.2f} MB"
        )

    def print_metrics(
        self,
        url: str,
        total_mb: float,
        total_time: float,
        avg_time: float,
        speed_mb_per_sec: float,
    ) -> None:
        """Prints speed test results using a clean, table for perfect alignment."""
        self.console.print(f"\n{self.fmt_split_line}")
        self.console.print(
            " [bold]SPEED TEST RESULTS[/]", style=f"bold {COLOR_PRIMARY}"
        )
        self.console.print(self.fmt_split_line)

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Metric", style=COLOR_DIM, justify="right")
        table.add_column("Value", style="bold")

        table.add_row("Target URL", url)
        table.add_row("Total requests", str(self.total_iterations))
        table.add_row("Total downloaded", f"{total_mb:.2f} MB")
        table.add_row("Total time", f"{total_time:.3f} sec")
        table.add_row("Average time", f"{avg_time:.3f} sec/request")

        table.add_row(
            "🥇 Avg Speed",
            f"{speed_mb_per_sec:.2f} MB/s",
            style=f"bold {COLOR_SUCCESS}",
        )

        self.console.print(table)
        self.console.print(f"{self.fmt_split_line}")
