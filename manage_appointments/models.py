from django.db import models

from manage_patients.models import Patient
from manage_doctors.models import Doctor
# Create your models here.

class Appointments(models.Model):
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE)    
    doctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.DateTimeField(null=True)
    status = models.CharField(max_length=255)
    
    def __str__(self):
        return f'Patient: {self.patientID} - Doctor: {self.doctorID} - date: {self.date}'