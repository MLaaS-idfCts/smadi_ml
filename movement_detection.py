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

    # initialize the first frame in the video stream
    avg = None
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = vs.read()
        frame = frame if args.get("video", None) is None else frame[1]
        text = "Unoccupied"
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            break
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # if the first frame is None, initialize it
        if avg is None:
            avg = gray.copy().astype("float")
            continue
        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(cv2.convertScaleAbs(avg), gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue

            text = "Occupied"

        if text == "Occupied":
            faces = face_recognition.face_locations(frame)
            if len(faces):
                for face in faces:
                    request_data = json.dumps((frame.tolist(), [face]))
                    print(request_data, type(frame))
                    requests.post(const.SERVER_ENDPOINT, request_data)
    # cleanup the camera and close any open windows
    vs.stop()


if __name__ == '__main__':
    movement_detection()
