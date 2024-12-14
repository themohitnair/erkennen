import os
from config import FACES_DIR, PICKLE
import pickle
import face_recognition


def name_faces():
    if os.path.exists(PICKLE):
        os.remove(PICKLE)
    encodings_dict = {}
    for filename in os.listdir(FACES_DIR):
        if filename.endswith(".png"):
            image_path = os.path.join(FACES_DIR, filename)

            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)

            if face_encodings:
                encoding = face_encodings[0]
                encodings_dict[tuple(encoding)] = input(
                    f"\nEnter the name of {filename}: "
                )

    with open("namedata.pkl", "wb") as file:
        pickle.dump(encodings_dict, file)
