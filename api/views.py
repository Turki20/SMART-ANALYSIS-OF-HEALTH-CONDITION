from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response # عشان يرجع كل الاستجابات
from rest_framework.decorators import api_view, permission_classes # عشان نحدد نوع الريكويست
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
import requests
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
from users.models import CustomUser
from .serializers import CustomUserSerialziers, PatientSerialziers, DoctorSerialziers, AppointmentsSerialziers, UpdateUserSerialziers, HealthDataSerializer
from manage_patients.models import Patient
from manage_doctors.models import Doctor
from manage_appointments.models import Appointments
from health_data.models import HealthData

@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # إنشاء التوكنات
        refresh = RefreshToken.for_user(user)
        
        # سيريالايزر بيانات المستخدم
        user_serializer = CustomUserSerialziers(user)
        if user.role == 'patient':
            patient = Patient.objects.select_related('userID').get(userID = user.id)
            patinet_serializer = PatientSerialziers(patient)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data,
                'patient': patinet_serializer.data,
            })
        elif user.role == 'doctor':
            doctor = Doctor.objects.select_related('userID').get(userID = user.id)
            doctor_serializer = DoctorSerialziers(doctor)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data,
                'doctor': doctor_serializer.data,
            })
        else:
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data,
            })
    else:
        return Response({'error': 'Invalid credentials'}, status=401)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_appintment(request, patinetID):
    appointments = Appointments.objects.select_related('patientID', 'doctorID').filter(patientID=patinetID)
    apps = AppointmentsSerialziers(appointments, many=True)
    return Response({
        'appointments': apps.data,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_appintment(request, doctorID):
    try:
        appointments = Appointments.objects.select_related('patientID', 'doctorID').filter(doctorID=doctorID)
        apps = AppointmentsSerialziers(appointments, many=True)
        return Response({
            'appointments': apps.data,
        })
    except Appointments.DoesNotExist:
        return Response({
            'mssage': 'لاتوجد مواعيد متاحة'
        })
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_data(request, patinetID):
    try:
        patient = Patient.objects.get(id=patinetID)
        ps = PatientSerialziers(patient)
        user = CustomUser.objects.get(username=patient.userID)
        us = CustomUserSerialziers(user)
        return Response({
            'user': us.data,
            'patinet': ps.data
        })
                
    except Patient.DoesNotExist:
        return Response({
            'mssage': 'المريض غير موجود'
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor_data(request, doctorID):    
    try:
        doctor = Doctor.objects.get(id=doctorID)
        ds = DoctorSerialziers(doctor)
        user = CustomUser.objects.get(username=doctor.userID)
        us = CustomUserSerialziers(user)
        return Response({
            'user': us.data,
            'doctor': ds.data
        })
    except Doctor.DoesNotExist:
        return Response({
            'mssage': 'الدكتور غير موجود'
        })
        
@swagger_auto_schema(method='post', request_body=AppointmentsSerialziers)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_appointment_pateient(request):    
    app = AppointmentsSerialziers(data=request.data)
    if app.is_valid():
        app.save()
        return Response(app.data)
    else:
        return Response({
            'mssage': 'البيانات المدخلة غير صحيحة او غير مكتملة'
        })
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_appointment(request, id):
    try:
        app = Appointments.objects.get(id=id)
        app.delete()
        return Response({
            'mssage': 'تم حذف الموعد بنجاح'
        })
    except Appointments.DoesNotExist:
        return Response({
            'mssage': 'سجل الموعد غير موجود'
        })
        
@swagger_auto_schema(method='patch', request_body=AppointmentsSerialziers)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_appointment_patient(request, id):
    try:
        appointment = Appointments.objects.get(id=id)
    except Appointments.DoesNotExist:
        return Response({'mssage': 'الموعد غير موجود'}, status=404)

    serializer = AppointmentsSerialziers(appointment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'mssage': 'تم تحديث الموعد بنجاح', 'data': serializer.data})
    else:
        return Response({'mssage': 'البيانات المدخلة غير صحيحة', 'errors': serializer.errors}, status=400)


@swagger_auto_schema(method='patch', request_body=UpdateUserSerialziers)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_data(request, id):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return Response({'mssage': 'المستخدم غير موجود'}, status=404)

    serializer = UpdateUserSerialziers(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'mssage': 'تم تحديث بيانات المستخدم بنجاح', 'data': serializer.data})
    else:
        return Response({'mssage': 'البيانات المدخلة غير صحيحة', 'errors': serializer.errors}, status=400)

@swagger_auto_schema(method='patch', request_body=PatientSerialziers)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_patient_data(request, id):
    try:
        patient = Patient.objects.get(id=id)
    except Patient.DoesNotExist:
        return Response({'mssage': 'المريض غير موجود'}, status=404)

    serializer = PatientSerialziers(patient, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'mssage': 'تم تحديث بيانات المريض بنجاح', 'data': serializer.data})
    else:
        return Response({'mssage': 'البيانات المدخلة غير صحيحة', 'errors': serializer.errors}, status=400)
   

from drf_yasg import openapi
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='الاسم الأول', example='محمد'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='اسم العائلة', example='أحمد'),
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='اسم المستخدم', example='mohamed123'),
        'password1': openapi.Schema(type=openapi.TYPE_STRING, description='كلمة المرور', example='StrongPassword123'),
        'password2': openapi.Schema(type=openapi.TYPE_STRING, description='تأكيد كلمة المرور', example='StrongPassword123'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='البريد الإلكتروني', example='mohamed@example.com'),
        'role': openapi.Schema(type=openapi.TYPE_STRING, description='admin, patient, doctor', example='admin, patient, or doctor'),
    },
    required=['first_name', 'last_name', 'username', 'password1', 'password2', 'email']
))
@api_view(['POST'])
@permission_classes([AllowAny])
def craete_user(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    username = request.data.get('username')
    role = request.data.get('role')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    email = request.data.get('email')
    

    if username == None or first_name == None or last_name == None or email == None or role == None:
        return Response({"message": "هناك بعض الحقول الغير مكتملة"}, status=400)
    
    if password1 != password2:
        return Response({'message': 'كلمتا المرور غير متطابقتين'}, status=400)

    if CustomUser.objects.filter(username=username).exists():
        return Response({'message': 'اسم المستخدم موجود بالفعل'}, status=400)

    user = CustomUser.objects.create(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        role=role,
    )
    user.set_password(password1)
    
    if role == 'admin':
        user.is_staff = True
        user.is_superuser = True

    user.save()
    
    if role == 'patient':
        Patient.objects.create(userID=user)
    elif role == 'doctor':
        Doctor.objects.create(userID=user)

   # us = CustomUserSerialziers()
    return Response({
        'message': 'تم إنشاء المستخدم بنجاح',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
        }
    })
    
@permission_classes([IsAuthenticated])  
class AnalyzeAudioAPIView(APIView):
    def post(self, request):
        audio_file = request.FILES.get('audio_file')
        
        if not audio_file:
            return Response({'error': 'No audio file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        files = {'audio_file': (audio_file.name, audio_file.read(), audio_file.content_type)}

        try:
            external_api_url = 'https://web-production-39fbc.up.railway.app/api/predict/'
            external_response = requests.post(external_api_url, files=files)
            
            if external_response.status_code == 200:
                result = external_response.json()
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'External API error', 'details': external_response.text}, status=external_response.status_code)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  
def healthdata_list_create(request):
    if request.method == 'GET':
        healthdata = HealthData.objects.all()
        serializer = HealthDataSerializer(healthdata, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HealthDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mssage": 'تمت الاضافه بنجاح'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  
def healthdata_detail(request, pk):
    if request.method == 'GET':
        healthdata = HealthData.objects.filter(patientID=pk)
        if not healthdata.exists():
            return Response({'error': 'No HealthData found for this patient'}, status=status.HTTP_404_NOT_FOUND)
        serializer = HealthDataSerializer(healthdata, many=True)
        return Response(serializer.data)

    try:
        healthdata = HealthData.objects.get(pk=pk)
    except HealthData.DoesNotExist:
        return Response({'error': 'HealthData not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = HealthDataSerializer(healthdata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        healthdata.delete()
        return Response({'message': 'HealthData deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
