from django.db import models

from django.conf import settings
# Create your models here.
class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ربط الطبيب مع المستخدم
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')
    availability = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Doctor {self.userID.username} -  Specialty: {self.specialty}"
