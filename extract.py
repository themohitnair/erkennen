import face_recognition
from PIL import Image
from config import FACES_DIR, SS_DIR
import logging
import os


def crop_and_store_faces():
    known_face_encodings = []

    for filename in os.listdir(SS_DIR):
        if filename.endswith(".png"):
            image_path = os.path.join(SS_DIR, filename)
            logging.info(f"Loaded {filename} for processing.")

            image = face_recognition.load_image_file(image_path)

            locs = face_recognition.face_locations(image)
            encs = face_recognition.face_encodings(image, locs)

            for i, (loc, enc) in enumerate(zip(locs, encs)):
                matches = face_recognition.compare_faces(known_face_encodings, enc)

                if True not in matches:
                    known_face_encodings.append(enc)

                    top, right, bottom, left = loc

                    face = image[top:bottom, left:right]
                    pil_image = Image.fromarray(face)

                    face_filename = f"{os.path.splitext(filename)[0]}_face_{i+1}.jpg"
                    output_path = os.path.join(FACES_DIR, face_filename)
                    pil_image.save(output_path)

                    logging.info(f"Saved {output_path} to {FACES_DIR} directory.")
                else:
                    logging.info(f"Duplicate face detected in {filename}. Skipping.")
        else:
            logging.info("Not a PNG. Skipping.")
