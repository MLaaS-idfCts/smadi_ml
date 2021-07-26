from django.db import models

# Create your models here.

class Soldier(models.Model):
    personal_number = models.CharField(max_length=8)
    commander_personal_number = models.CharField(max_length=8)
    phone_number = models.CharField(max_length=11)
    mac_bluetooth = models.CharField(max_length=12)
    device_name = models.CharField(max_length=12)
    face_photo = models.ImageField(upload_to="../../smadi_ml")

    def __str__(self):
        return self.id