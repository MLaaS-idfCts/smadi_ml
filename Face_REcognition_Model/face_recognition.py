import face_recognition
import os

folder_name = 'smadi_ml'


def get_avocado_label(arr, locations):

    avocado_images = []
    images = os.listdir(folder_name)
    for image in images:
        img = face_recognition.load_image_file("smadi_ml/" + image)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        avocado_face_encoding = face_recognition.face_encodings(img)[0]
        avocado_images.append(avocado_face_encoding)

    # Initialize some variables
    names = [image.replace('.jpeg', '') for image in images]

    # Find all the faces and face encodings in the current frame of video
    avocado_encodings = face_recognition.face_encodings(arr, locations)

    # Loop over each face found in the frame to see if it's someone we know.
    avocado_names = []
    for avocado_encoding in avocado_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(avocado_images, avocado_encodings, tolerance=0.5)
        name = []
        for loc in range(len(match)):
            if match[loc]:
                name.append(names[loc])
        if not name:
            name = ['unknown']
        avocado_names.append(name)

        return [format(n) for n in name]
    pass
