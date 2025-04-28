from django.db import models

from manage_patients.models import Patient
# Create your models here.

class HealthData(models.Model):
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    coughSound = models.FileField(upload_to='cough_sounds/', null=True, blank=True)
    analysisResult = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"HealthData {self.id} - {self.analysisResult}"