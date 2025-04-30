from django.db import models

from manage_patients.models import Patient
from manage_doctors.models import Doctor
# Create your models here.

class Appointments(models.Model):
    STATUS_CHOICES = [
        ('available', 'متاح'),
        ('booked', 'محجوز'),
    ]
    patientID = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)    
    doctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    
    def __str__(self):
        return f'Doctor: {self.doctorID} - Date: {self.date} - Time: {self.time} - Status: {self.get_status_display()}'
    