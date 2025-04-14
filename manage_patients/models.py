from django.db import models

from django.conf import settings
# Create your models here.

class Patient(models.Model):
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ربط المريض مع المستخدم
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    healthdataa = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Patient {self.userID.username} - Age: {self.age}"
