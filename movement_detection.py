# import the necessary packages
import face_recognition
import imutils
import time
import const
import requests
from imutils.video import VideoStream


def movement_detection_loop():
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    count = 0

    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = vs.read()

        if frame is None:
            raise IOError

        frame = imutils.resize(frame, width=500)

        faces = face_recognition.face_locations(frame)
        if len(faces):
            for face in faces:
                requests.post(url=f'{const.SERVER_ENDPOINT}/api/report_by_image/', data={
                    'image': frame.tolist(),
                    'face': list(face),
                    'size': list(frame.shape)
                })
                count += 1
        if count < 3:
            wait = 0
        else:
            wait = 1
            count = 0
        time.sleep(wait)


if __name__ == '__main__':
    movement_detection_loop()
