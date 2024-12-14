import pickle
from config import PICKLE
import face_recognition
from PIL import ImageDraw, ImageGrab, Image


def capture_and_annotate():
    with open(PICKLE, "rb") as file:
        enc_name_dict: dict = pickle.load(file)

    known_face_encodings = list(enc_name_dict.keys())
    known_face_names = list(enc_name_dict.values())

    image = ImageGrab.grab()

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    pil_image = Image.fromarray(image)
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

        text_width, text_height = draw.textsize(name)
        draw.rectangle(
            ((left, bottom - text_height), (right, bottom)), fill=(0, 0, 255)
        )
        draw.text((left + 6, bottom - text_height), name, fill=(255, 255, 255))
