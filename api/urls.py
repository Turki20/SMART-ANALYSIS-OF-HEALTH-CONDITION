from django.urls import path, re_path
from . import views as api

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="شرح لجميع الاندبوينتس طبعا يحتاج توكن",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # athentication endpoints
    path("custom_login/", api.custom_login, name="custom_login"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # get endpoints
    path('patient_appintments/<int:patinetID>/', api.patient_appintment),
    path('doctor_appintments/<int:doctorID>/', api.doctor_appintment),
    path('get_patinet/<int:patinetID>/', api.get_patient_data),
    path('get_doctor/<int:doctorID>/', api.get_doctor_data),
    
    # post endpoints
    path('add_patient_appointment/', api.add_appointment_pateient),
    path('create_user/', api.craete_user),
    
    # delete endpoints
    path('delete_appointment/<int:id>/', api.delete_appointment),
    
    # patch endpoints
    path('update_appointment/<int:id>/', api.update_appointment_patient),
    path('update_user_data/<int:id>/', api.update_user_data),
    path('update_patient_data/<int:id>/', api.update_patient_data),
    
    # post endpoints for AI analysis
    path('analyze_audio/', api.AnalyzeAudioAPIView.as_view(), name='analyze_audio'),
    
    # health data endpoints
    path('healthdata/', api.healthdata_list_create, name='healthdata_list_create'),
    path('healthdata/<int:pk>/', api.healthdata_detail, name='healthdata_detail'),
]
