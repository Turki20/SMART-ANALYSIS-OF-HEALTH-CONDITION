from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    
    def __str__(self):
        return self.username
    
    
from django.conf import settings

class AdminLog(models.Model):
    adminID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.id} by {self.adminID.username} - {self.action}"
