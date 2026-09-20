import logging

from src import run_speed_test

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

log = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        log.info("Running speed test...")
        run_speed_test()
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt received, exiting...")
    except Exception as e:
        log.error(f"An error occurred: {e}", exc_info=True)
