import logging
import time

import httpx

from .ui import UIClient

log = logging.getLogger(__name__)


def download_single_request(
    ui_client: UIClient,
    url: str,
    iteration: int,
    file_size: int,
    chunk_size: int,
) -> tuple[float, int]:
    """Download single request and return time and downloaded bytes."""
    log.info("Downloading %s", url)
    start_time = time.perf_counter()
    downloaded_bytes = 0

    with (
        ui_client.progress(iteration=iteration) as progress,
        httpx.Client(follow_redirects=True, timeout=30) as client,
        client.stream("GET", url) as response,
    ):
        task_id = progress.add_task("Downloading", total=file_size)
        response.raise_for_status()

        for chunk in response.iter_bytes(chunk_size=chunk_size):
            if chunk:
                downloaded_bytes += len(chunk)
                progress.update(task_id, completed=downloaded_bytes)

    end_time = time.perf_counter()
    return end_time - start_time, downloaded_bytes


def get_file_size(url: str) -> int | None:
    """Get file size from content-length header."""
    log.info("Getting file size from %s", url)
    try:
        with httpx.Client(follow_redirects=True, timeout=10) as client:
            response = client.head(url)
            response.raise_for_status()
            content_length = response.headers.get("content-length")

            return int(content_length) if content_length else None
    except httpx.HTTPError:
        return None


def get_and_validate_url(ui_client: UIClient) -> str | None:
    """Get and validate URL from user input."""
    url = ui_client.ask_url()
    if not url.startswith(("http://", "https://")):
        ui_client.print_error("Invalid URL.")
        return None
    return url


def get_and_validate_file_size(ui_client: UIClient, url: str) -> int | None:
    """Get file size and validate it."""
    file_size = get_file_size(url)
    if not file_size:
        ui_client.print_error(
            "Failed to get file size (Content-Length header is missing)"
        )
        return None
    return file_size


def run_download_loop(
    ui_client: UIClient,
    url: str,
    iterations: int,
    file_size: int,
    chunk_size: int,
) -> tuple[float, int]:
    """Run download loop for given url and iterations."""
    total_time = 0.0
    total_bytes = 0

    for iteration in range(1, iterations + 1):
        try:
            req_time, req_bytes = download_single_request(
                ui_client=ui_client,
                url=url,
                iteration=iteration,
                file_size=file_size,
                chunk_size=chunk_size,
            )
            total_time += req_time
            total_bytes += req_bytes
            ui_client.print_info_downloaded(req_time, req_bytes)
        except httpx.HTTPError as e:
            ui_client.print_error(f"Request error {iteration}: {e}")

    return total_time, total_bytes
