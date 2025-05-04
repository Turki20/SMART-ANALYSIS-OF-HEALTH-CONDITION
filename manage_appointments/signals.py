from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointments
from chat.models import Chat

@receiver(post_save, sender=Appointments)
def create_chat_when_patient_added(sender, instance, created, **kwargs):
    if instance.patientID and not instance.chat:
        chat = Chat.objects.create()
        chat.participants.add(instance.patientID.userID)
        chat.participants.add(instance.doctorID.userID)
        instance.chat = chat
        instance.save()
        print(f"Chat created for appointment {instance.id} between {instance.patientID.userID.username} and {instance.doctorID.userID.username}.")