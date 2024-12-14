import time
import logging
import signal
import sys
from screenshot import capture
from extract import crop_and_store_faces


def on_interrupt(signum, frame):
    logging.info("Interrupt received!")
    crop_and_store_faces()
    sys.exit(0)


signal.signal(signal.SIGINT, on_interrupt)


def service():
    while True:
        capture()
        time.sleep(5)


if __name__ == "__main__":
    service()
