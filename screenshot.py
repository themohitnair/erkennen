from PIL import ImageGrab
from config import SS_DIR
import os
import numpy as np
import face_recognition
import logging
import time
import config

logger = logging.getLogger(__name__)

def capture():
    os.makedirs(SS_DIR, exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    image_path = os.path.join(SS_DIR, f"screenshot_{timestamp}.png")

    screenshot = ImageGrab.grab()

    image_np = np.array(screenshot)
    face_locations = face_recognition.face_locations(image_np)
    if len(face_locations) == 0:
        logger.info("No faces detected in the screenshot.")
        return

    screenshot.save(image_path, format="PNG", optimize=True)
    logger.info(f"Screenshot image {image_path} saved.")
