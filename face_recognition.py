import os
from pathlib import Path
import face_recognition


def load_face_encodings_from_folder(folder_path):
    """Load all face encodings from images in the specified folder."""
    face_encodings = []
    for image_path in Path(folder_path).glob('*.jpg'):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            face_encodings.append(encodings[0])
    return face_encodings


def find_matching_faces(reference_encodings, target_folder):
    """Find all images in the target folder that contain faces matching the reference encodings."""
    matched_images = []
    for image_path in Path(target_folder).glob('*.jpg'):
        image = face_recognition.load_image_file(image_path)
        target_encodings = face_recognition.face_encodings(image)

        for target_encoding in target_encodings:
            matches = face_recognition.compare_faces(reference_encodings, target_encoding)
            if any(matches):
                matched_images.append(image_path)
                break  # Stop after finding one match in this image
    return matched_images


if __name__ == '__main__':
#    reference_folder = input("Enter the path to the folder with reference pictures: ")
#    target_folder = input("Enter the path to the folder to search for matching faces: ")

    reference_folder = r"C:\Users\marti\Desktop\24_SortPictures\pictures_of_Martin"
    target_folder = r"C:\Users\marti\Desktop\24_SortPictures\pictures_of_Martin_and_other"

    # Load reference face encodings
    reference_encodings = load_face_encodings_from_folder(reference_folder)
    if not reference_encodings:
        print("No faces found in the reference folder.")
        exit()

    # Find matching faces in the target folder
    matched_images = find_matching_faces(reference_encodings, target_folder)

    if matched_images:
        print("Found matching images:")
        for image_path in matched_images:
            print(image_path)
    else:
        print("No matching images found.")
