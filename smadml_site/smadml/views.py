import os
import subprocess

import numpy as np
from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from  .models import Soldier
from .send_report import send_report
from PIL import Image
import cv2

from .Face_REcognition_Model.face_recognition import get_avocado_label

faces_path = '/tmp/pycharm_project_298/smadi_ml/'
# Create your views here.
def get_id_from_image(image, locations):
    return get_avocado_label(image, locations)


@api_view(http_method_names=["POST"])
def report_by_image(request):
    # TODO: Matrix of (r,g,b) tuples + location of face
    data = dict(request.data)
    image = data["image"]
    locations = [tuple([int(datum) for datum in data["face"]])]
    size = data["size"]
    image = [eval(datum) for datum in image]
    image_data = np.array(image, dtype=np.uint8)
    image_data.resize((int(size[0]), int(size[1]), int(size[2])))
    id = get_id_from_image(image_data, locations)
    try:
        output = subprocess.run(["python3", "smadml/showcase.py"], stdout=subprocess.PIPE)
    except Exception as e:
        return Response("Error signing, please try again", status=500)
    # TODO: error in failure
    return Response("Reported user", status=200)


def get_id_from_mac(mac):
    try:
        soldier = Soldier.objects.filter(mac_bluetooth=mac).get()
        return soldier.id
    except Exception as e:
        pass
        # TODO:
    return -1

@api_view(http_method_names=["POST"])
def report_by_bluetooth(request):
    mac = request.data["mac"]
    device_name = request.data["device_name"]
    id = get_id_from_mac(mac)
    if id == -1:
        return Response("User does not exist", status=400)

    try:
        output = subprocess.run(["python3", "smadml/showcase.py"], stdout=subprocess.PIPE)
    except Exception as e:
        return Response("Error signing, please try again", status=500)
    # TODO: Error on failure
    return Response("User reported", status=200)


@api_view(http_method_names=["POST"])
@parser_classes([JSONParser])
def register_user(request):
    data = request.data
    face_photo_bytes = np.asarray(data["photo"]["py/seq"], dtype=np.uint8)
    image = cv2.imdecode(face_photo_bytes, cv2.IMREAD_COLOR)
    filename = os.path.join("tmp", "pycharm_project_298", "smadi_ml", "smadi_ml",
                            f"{data['personal_number']}.jpg")
    cv2.imwrite(os.path.join(os.path.dirname(__file__), filename), image)
    soldier = Soldier(personal_number=data["personal_number"],
                      phone_number=data["phone_number"],
                      commander_personal_number=data["commander_personal_number"],
                      commander_phone_number=data["commander_phone_number"],
                      mac_bluetooth=data["mac_bluetooth"],
                      device_name=data["device_name"],
                      face_photo=image)
    soldier.save()
    # TODO: error on invalid user
    return Response("User created", status=201)

def report_by_id(id: str):
    send_report(id)