import face_recognition
import os
import cv2

print("Loading known face image(s)")
obama_images = []
images = os.listdir('smadi_ml')
for image in images:
    if 'test' in image or 'test_4' in image:
        continue
    img = face_recognition.load_image_file("smadi_ml/" + image)
    obama_face_encoding = face_recognition.face_encodings(img)[0]
    obama_images.append(obama_face_encoding)

# Initialize some variables
face_locations = []
face_encodings = []
names = [image.replace('.jpg', '').replace('.PNG', '') for image in images if image != 'family.jpg']

print("Capturing image.")
# Grab a single frame of video from the RPi camera as a numpy array
output = face_recognition.load_image_file('smadi_ml/test_4.jpg')

# Find all the faces and face encodings in the current frame of video
face_locations = face_recognition.face_locations(output)
print("Found {} faces in image.".format(len(face_locations)))
face_encodings = face_recognition.face_encodings(output, face_locations)

# Loop over each face found in the frame to see if it's someone we know.
face_names = []
for face_encoding in face_encodings:
    # See if the face is a match for the known face(s)
    match = face_recognition.compare_faces(obama_images, face_encoding, tolerance=0.5)
    name = []

    for loc in range(len(match)):
        if match[loc]:
            name.append(names[loc])
    if not name:
        name = ['unknown']
    face_names.append(name)

    for n in name:
        print("I see someone named {}!".format(n))

    # Display the results
for (top, right, bottom, left), name in zip(face_locations, face_names):
    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    top *= 1
    right *= 1
    bottom *= 1
    left *= 1

    # Draw a box around the face
    cv2.rectangle(output, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    cv2.rectangle(output, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(output, str(name[0]), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

# Display the resulting image
cv2.imshow('test', output)

cv2.waitKey(0)
