from users.models import CustomUser
from manage_patients.models import Patient
from manage_doctors.models import Doctor
from manage_appointments.models import Appointments
from rest_framework import serializers

class CustomUserSerialziers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
    
        
class UpdateUserSerialziers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
class PatientSerialziers(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorSerialziers(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        
class AppointmentsSerialziers(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = '__all__'