from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from users.models import AdminLog
from manage_doctors.models import Doctor
from manage_patients.models import Patient
from manage_appointments.models import Appointments
# Create your views here.
from django.db.models import Count

@login_required(login_url="/user/login/")
@staff_member_required
def home_page(request):
    adminLog = AdminLog.objects.order_by('-timestamp')[:10]
    numberOfPatient = Patient.objects.count()
    numberOfDoctor = Doctor.objects.count()
    numberOfApp = Appointments.objects.count()                
    context = {
        'logs': adminLog,
        'numberOfPatient': numberOfPatient,
        'numberOfDoctor': numberOfDoctor,
        'numberOfApp': numberOfApp,
    }
    return render(request, 'home.html', context)