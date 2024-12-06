import os
from datetime import datetime
from PIL import ImageGrab, Image
import face_recognition


def screenshot() -> None:
    os.makedirs("screenshots", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"screenshots/screenshot_{timestamp}.png"

    screenshot = ImageGrab.grab()

    screenshot.save(file_name)


def extract_faces_from_directory(input_dir: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_dir, filename)

            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)

            if not face_locations:
                print(f"No faces detected in {filename}!")
                continue

            for i, (top, right, bottom, left) in enumerate(face_locations):
                face_image = image[top:bottom, left:right]

                pil_image = Image.fromarray(face_image)

                # Resize the image to have a width of 512 while maintaining aspect ratio
                aspect_ratio = pil_image.height / pil_image.width
                new_width = 144
                new_height = int(new_width * aspect_ratio)
                resized_face = pil_image.resize((new_width, new_height), Image.LANCZOS)

                face_filename = f"{os.path.splitext(filename)[0]}_face_{i+1}.png"
                face_file_path = os.path.join(output_dir, face_filename)

                resized_face.save(face_file_path)
                print(f"Saved resized face {i+1} from {filename} as {face_file_path}")


if __name__ == "__main__":
    output_dir = "extracted_faces"
    extract_faces_from_directory("screenshots", output_dir)
