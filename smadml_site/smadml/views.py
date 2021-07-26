from django.shortcuts import render
from rest_framework.decorators import api_view
from  .models import Soldier
from ..smadml.send_report import send_report
from PIL import Image

faces_path = "../../smadi_ml"
# Create your views here.
def get_id_from_image(image):
    pass


@api_view()
def report_by_image(request):
    # TODO: Matrix of (r,g,b) tuples + location of face
    image = request.data["image"]
    id = get_id_from_image(image)
    report_by_id(id)
    pass


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


@api_view()
def register_user(request):
    data = request.data
    soldier = Soldier(id=data["id"], commander_id=data["commander_id"],
                      phone_number=data["phone_number"],
                      mac_bluetooth=data["mac_bluetooth"],
                      device_name=data["device_name"],
                      face_photo=Image.open(data["image"]))
    soldier.save()


def report_by_id(id: str):
    send_report(id)