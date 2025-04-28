from django.urls import path
from . import views

urlpatterns = [
    path('', views.healthdata_list, name='healthdata_list'),
    path('delete/<int:pk>/', views.delete_healthdata, name='delete_healthdata'),
]
