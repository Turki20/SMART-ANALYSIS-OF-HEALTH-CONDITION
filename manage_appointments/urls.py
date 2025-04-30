from django.urls import path
from . import views as a

urlpatterns = [
    path('all_appintments/', a.all_appoinnments, name='all_appintments'),
    path('create_appointment/', a.create_appointment, name='create_appointment'),
    path('delet_appintment/<int:id>/', a.delete_appointment, name='delet_appintment'),
    path('update_appintment/<int:id>/', a.update_appointment, name='update_appintment'),
    path('generate_appointments/', a.generate_fixed_appointments, name='generate_fixed_appointments'),
]
