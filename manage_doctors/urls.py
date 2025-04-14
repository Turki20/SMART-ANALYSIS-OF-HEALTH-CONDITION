from django.urls import path
from . import views as d
urlpatterns = [
    path('all_doctors/', d.all_doctors, name='all_doctors'),
    path('create_doctor/', d.create_doctor, name='create_doctor'),
    path('delete_doctor/<int:id>/', d.delete_doctor, name='delete_doctor'),
    path('update_doctor/<int:id>/', d.update_doctor, name='update_doctor'),
]
