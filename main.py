import time
import logging
import signal
import sys
from screenshot import capture
from extract import crop_and_store_faces
from name import name_faces
from annotate import capture_and_annotate

in_gather_mode = False


def main():
    global in_gather_mode
    choice = input(
        "Choose a mode: \n[g] -> Gather\n[a] -> Annotate\nEnter your choice [G/a]: "
    )
    if choice.lower() == "a":
        annotate_service()
    else:
        in_gather_mode = True
        gather_service()


def on_interrupt(signum, frame):
    global in_gather_mode
    logging.info("Interrupt received!")

    if in_gather_mode:
        logging.info("Gather service interrupted. Processing images...")
        crop_and_store_faces()
        name_faces()
        sys.exit(0)
    else:
        logging.info("Annotate service interrupted. Exiting normally...")
        sys.exit(0)


signal.signal(signal.SIGINT, on_interrupt)


def annotate_service():
    while True:
        capture_and_annotate()


def gather_service():
    while True:
        time.sleep(5)
        capture()


if __name__ == "__main__":
    main()
