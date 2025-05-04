from users.models import CustomUser
from manage_patients.models import Patient
from manage_doctors.models import Doctor
from manage_appointments.models import Appointments
from rest_framework import serializers
from health_data.models import HealthData

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
        
class HealthDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthData
        fields = ['patientID', 'analysisResult', 'timestamp', 'date']
        
        
        
from chat.models import Message, Chat
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.id')  # نملأها تلقائيًا من request.user

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'timestamp']