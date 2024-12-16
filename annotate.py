import pickle
from config import PICKLE, ANNOTATED
import face_recognition
import logging
from PIL import ImageDraw, ImageGrab, Image
import time
import os
import numpy as np

logger = logging.getLogger(__name__)


enc_name_dict       : dict | None = None
known_face_encodings: list        = None
known_face_names    : list        = None

def capture_and_annotate():
    global enc_name_dict
    global known_face_encodings
    global known_face_names
    if enc_name_dict is None:
        try:
            with open(PICKLE, "rb") as file:
                enc_name_dict = pickle.load(file)
                logger.info(f"Loaded {PICKLE}.")
        except FileNotFoundError:
            logger.error("Pickle file not found. Have you gathered the images first?")
            raise

        known_face_encodings = [
            np.array(encoding_tuple) for encoding_tuple in enc_name_dict.keys()
        ]
        known_face_names = list(enc_name_dict.values())

    os.makedirs(ANNOTATED, exist_ok=True)

    time.sleep(5)
    image = ImageGrab.grab()
    logger.info("Captured screenshot for annotation.")

    image_np = np.array(image)

    face_locations = face_recognition.face_locations(image_np)
    if len(face_locations) == 0:
        logger.info("No faces detected in the screenshot.")
        return

    face_encodings = face_recognition.face_encodings(image_np, face_locations)

    pil_image = Image.fromarray(image_np)
    draw = ImageDraw.Draw(pil_image)

    for (top, right, bottom, left), face_encoding in zip(
        face_locations, face_encodings
    ):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255), width=2)

        text_bbox = draw.textbbox((left + 6, bottom - 20), name)
        text_height = text_bbox[3] - text_bbox[1]

        draw.rectangle(
            ((left, bottom - text_height), (right, bottom)), fill=(0, 0, 255)
        )
        draw.text((left + 6, bottom - text_height), name, fill=(255, 255, 255))

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    annotated_image_path = os.path.join(ANNOTATED, f"annotated_{timestamp}.png")
    pil_image.save(annotated_image_path)

    logger.info(f"Annotated image saved at: {annotated_image_path}")
