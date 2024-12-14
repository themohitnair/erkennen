from PIL import ImageGrab
from config import SS_DIR
import os
import logging
import time


def capture():
    os.makedirs(SS_DIR, exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    image_path = os.path.join(SS_DIR, f"screenshot_{timestamp}.png")

    screenshot = ImageGrab.grab()

    screenshot.save(image_path, format="PNG", optimize=True)
    logging.info(f"Screenshot image {image_path} saved.")


if __name__ == "__main__":
    time.sleep(5)
    capture()
