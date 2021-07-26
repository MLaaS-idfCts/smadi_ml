
# import the necessary packages
import face_recognition
import argparse
import imutils
import time
import const
import requests
import json
import cv2
from imutils.video import VideoStream


def movement_detection_loop():
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    count = 0

    # initialize the first frame in the video stream
    avg = None
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = vs.read()
        text = "Unoccupied"

        if frame is None:
            raise IOError

        frame = imutils.resize(frame, width=500)

        faces = face_recognition.face_locations(frame)
        if len(faces):
            for face in faces:
                request_data = json.dumps((frame.tolist(), [face]))
                print(request_data, type(frame))
                requests.post(const.SERVER_ENDPOINT, request_data)
                count += 1
        if count < 3:   
            wait = 0
        else:
            wait = 1
            count = 0
        time.sleep(wait)


if __name__ == '__main__':
    movement_detection_loop()
