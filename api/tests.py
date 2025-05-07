from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from manage_patients.models import Patient
from manage_doctors.models import Doctor
from manage_appointments.models import Appointments
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

class UserViewsTests(APITestCase):
    def setUp(self):
        self.patient_user = CustomUser.objects.create_user(username='patient1', password='test1234', role='patient')
        self.doctor_user = CustomUser.objects.create_user(username='doctor1', password='test1234', role='doctor')

        self.patient = Patient.objects.create(user=self.patient_user, age=30, gender='M', health_condition='Good')
        self.doctor = Doctor.objects.create(user=self.doctor_user, specialty='Cardiology')

        self.appointment = Appointments.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date_time=datetime.now(),
            status='pending'
        )

        self.login_url = reverse('custom_login')
        self.register_url = reverse('register')
        self.patient_appointment_url = reverse('patient_appointment')
        self.doctor_appointment_url = reverse('doctor_appointment')
        self.refresh_url = reverse('token_refresh')
        self.update_appointment_url = reverse('update_appointment', args=[self.appointment.id])

    def get_auth_headers(self, user):
        refresh = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {str(refresh.access_token)}'}

    def test_custom_login_success(self):
        data = {'username': 'patient1', 'password': 'test1234'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_custom_login_fail(self):
        data = {'username': 'patient1', 'password': 'wrongpass'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_success(self):
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'role': 'patient',
            'age': 25,
            'gender': 'F',
            'health_condition': 'Excellent'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_missing_data(self):
        data = {'username': 'nouser', 'password': 'nopass'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_appointment_view(self):
        headers = self.get_auth_headers(self.patient_user)
        data = {'patient_id': self.patient.id}
        response = self.client.post(self.patient_appointment_url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_doctor_appointment_view(self):
        headers = self.get_auth_headers(self.doctor_user)
        data = {'doctor_id': self.doctor.id}
        response = self.client.post(self.doctor_appointment_url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_appointment(self):
        headers = self.get_auth_headers(self.patient_user)
        data = {'status': 'confirmed'}
        response = self.client.patch(self.update_appointment_url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'confirmed')

    def test_token_refresh(self):
        refresh = RefreshToken.for_user(self.patient_user)
        response = self.client.post(self.refresh_url, {'refresh': str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
