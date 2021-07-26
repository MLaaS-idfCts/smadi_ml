from django.shortcuts import render
from rest_framework.decorators import api_view
from  .models import Soldier
from ..smadml.send_report import send_report
from PIL import Image

from ..Face_REcognition_Model.face_recognition import get_avocado_label

faces_path = "../../smadi_ml"
# Create your views here.
def get_id_from_image(image, locations):
    return get_avocado_label(image, locations)


@api_view()
def report_by_image(request):
    # TODO: Matrix of (r,g,b) tuples + location of face
    image = request.data["image"]
    locations = request.data["locations"]
    id = get_id_from_image(image, locations)
    report_by_id(id)
    # TODO: response


def get_id_from_mac(mac):
    try:
        soldier = Soldier.objects.filter(mac_bluetooth=mac).get()
        return soldier.id
    except Exception as e:
        pass
        # TODO:
    return -1

@api_view()
def report_by_bluetooth(request):
    mac = request.data["mac"]
    device_name = request.data["device_name"]
    id = get_id_from_mac(mac)
    report_by_id(id)


@api_view(http_method_names=["POST"])
def register_user(request):
    data = request.data
    soldier = Soldier(personal_number=data["personal_number"],
                      commander_personal_number=data["commander_personal_number"],
                      phone_number=data["phone_number"],
                      mac_bluetooth=data["mac_bluetooth"],
                      device_name=data["device_name"],
                      face_photo=Image.open(data["image"]))
    soldier.save()


def report_by_id(id: str):
    send_report(id)