import logging

from .misc import get_and_validate_file_size, get_and_validate_url, run_download_loop
from .ui import UIClient

log = logging.getLogger(__name__)

BYTES_IN_MB = 1024 * 1024
REQUESTS_COUNT = 10
CHUNK_SIZE = 8192


def run_speed_test(iterations: int = REQUESTS_COUNT) -> None:
    """Run speed test for given url."""
    ui_client = UIClient(total_iterations=iterations, bytes_in_mb=BYTES_IN_MB)
    ui_client.print_starting_header()

    # 1. Valadate url
    url: str | None = get_and_validate_url(ui_client)
    if not url:
        return

    # 2. Valadate file size
    file_size: int | None = get_and_validate_file_size(ui_client, url)
    if not file_size:
        return

    # 3. Show speed test params
    ui_client.print_speed_test_params(url=url, file_size=file_size)

    # 4. Show loop downloading
    total_time, total_bytes = run_download_loop(
        ui_client,
        url,
        iterations,
        file_size,
        chunk_size=CHUNK_SIZE,
    )

    # 5. Calculate and print metrics
    avg_time = total_time / iterations
    total_mb = total_bytes / BYTES_IN_MB
    speed_mb_per_sec = total_mb / total_time if total_time > 0 else 0.0

    ui_client.print_metrics(
        url=url,
        total_mb=total_mb,
        total_time=total_time,
        avg_time=avg_time,
        speed_mb_per_sec=speed_mb_per_sec,
    )
