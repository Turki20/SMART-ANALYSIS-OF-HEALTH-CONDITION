from django.db import models

from django.conf import settings
# Create your models here.


class Doctor(models.Model):
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ربط الطبيب مع المستخدم
    specialization = models.CharField(max_length=255, blank=True, null=True)
    availability = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Doctor {self.userID.username} - Specialization: {self.specialization}"
