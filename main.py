import time
import logging
import signal
import sys
import typer
import log_config
from screenshot import capture
from extract import crop_and_store_faces
from name import name_faces
from annotate import capture_and_annotate

logger = logging.getLogger(__name__)

in_gather_mode = False

app = typer.Typer()

def on_interrupt(signum, frame):
    global in_gather_mode
    logger.info("Interrupt received!")

    if in_gather_mode:
        logger.info("Gather service interrupted. Processing images...")
        crop_and_store_faces()
        name_faces()
        sys.exit(0)
    else:
        logger.info("Annotate service interrupted. Exiting normally...")
        sys.exit(0)

signal.signal(signal.SIGINT, on_interrupt)

@app.command()
def annotate():
    logger.info("Starting annotation service...")
    while True:
        capture_and_annotate()

@app.command()
def gather():
    logger.info("Starting gather service...")
    global in_gather_mode
    in_gather_mode = True
    while True:
        time.sleep(5)
        capture()

if __name__ == "__main__":
    app()
