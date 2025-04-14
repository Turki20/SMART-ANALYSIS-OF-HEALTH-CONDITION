from django.urls import path
from . import views as p
urlpatterns = [
    path('all_patients/', p.all_pateints, name='all_patients'),
    path('create_patient/', p.create_patient, name='create_patient'),
    path('delete_patient/<int:userID>/', p.delete_patient, name='delete_patient'),
    path('update_patient/<int:id>/', p.update_patient, name='update_patient'),
]
