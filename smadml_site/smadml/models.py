from django.db import models

# Create your models here.

class Soldier(models.Model):
    personal_number = models.CharField(max_length=8)
    commander_personal_number = models.CharField(max_length=8, null=True)
    phone_number = models.CharField(max_length=11)
    commander_phone_number = models.CharField(max_length=11, null=True)
    mac_bluetooth = models.CharField(max_length=12)
    device_name = models.CharField(max_length=12)
    face_photo = models.CharField(max_length=200)

    def __str__(self):
        return self.personal_number