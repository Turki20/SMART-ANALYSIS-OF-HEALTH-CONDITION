from django.shortcuts import render, redirect, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

# Create your views here.
from .models import Appointments
from .forms import CreatAppointment, UpdateAppointment
from manage_doctors.models import Doctor

from datetime import date, time, timedelta, datetime

@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def all_appoinnments(request):
    app = Appointments.objects.select_related('patientID', 'doctorID').all()
    context = {
        'app': app,
    }
    return render(request, 'all_appointment.html', context)

@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
@csrf_exempt
def create_appointment(request):
    if request.method == 'POST':
        form = CreatAppointment(request.POST)
        if form.is_valid():
            if form.cleaned_data['patientID'] != None:
                if form.cleaned_data['patientID'].age == None:
                    messages.error(request, 'سجل بيانات المريض اولا!')
            elif form.cleaned_data['doctorID'].specialty == None:
                messages.error(request, 'اكمل تسجيل بيانات الدكتور!')
            else:
                form.save()
                messages.success(request, 'تمت اضافة الموعد بنجاح')
            return redirect('/appointment/create_appointment/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('/appointment/create_appointment/')
    else:
        form = CreatAppointment()
    return render(request, 'create_appintment.html', {'form': form})


@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def delete_appointment(request, id):
    try:
        app = Appointments.objects.get(id=id)
        app.delete()
        messages.success(request, 'تم حذف الموعد بنجاح!')
    except Appointments.DoesNotExist:
        messages.error(request, 'لم يتم حذف الموعد المحدد!')
    return redirect('/appointment/all_appintments/')

@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def update_appointment(request, id):
    app = Appointments.objects.get(id=id)
    
    if request.method == 'POST':
        form = UpdateAppointment(request.POST, instance=app)
        if form.is_valid():
            if form.cleaned_data['patientID'] != None:
                if form.cleaned_data['patientID'].age == None:
                    messages.error(request, 'سجل بيانات المريض اولا!')
                    return redirect(f'/appointment/update_appintment/{id}')
                
            if form.cleaned_data['doctorID'].specialty == None:
                messages.error(request, 'اكمل تسجيل بيانات الدكتور!')
            else:
                form.save()
                messages.success(request, 'تم تحديث الموعد بنجاح!')
            return redirect(f'/appointment/update_appintment/{id}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    
        return redirect(f'/appointment/update_appintment/{id}/')
    else:
        form = UpdateAppointment(instance=app)

    return render(request, 'update_appointment.html', {'form': form, 'id':id})


@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def generate_fixed_appointments(request):
    days_to_generate = 7
    start_date = date.today()
    hours = [9, 10, 11, 12, 13, 14, 15]
    created_count = 0

    no_specialty_count = Doctor.objects.filter(specialty__isnull=True).count()
    
    for doctor in Doctor.objects.filter(specialty__isnull=False):
        for i in range(days_to_generate):
            appointment_date = start_date + timedelta(days=i)
            if appointment_date.weekday() in [4, 5]:
                continue

            for hour in hours:
                appointment_datetime = datetime.combine(appointment_date, time(hour, 0))

                obj, created = Appointments.objects.get_or_create(
                    doctorID=doctor,
                    date=appointment_date,
                    time=appointment_datetime,  # ← هنا الفرق
                    defaults={'status': 'available'}
                )
                if created:
                    created_count += 1

    if created_count > 0:
        messages.success(request, f'تم إنشاء {created_count} موعداً ثابتاً.')
    else:
        messages.success(request, 'لا يوجد مواعيد جديدة لإنشائها.')
    if no_specialty_count > 0:
        messages.error(request, f'تم تجاهل {no_specialty_count} طبيبًا بدون تخصص.')
    return redirect('/appointment/all_appintments/')