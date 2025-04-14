from django.shortcuts import render, redirect, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

# Create your views here.
from .models import Appointments
from .forms import CreatAppointment, UpdateAppointment

@login_required(login_url="/admin/login/")
@staff_member_required
def all_appoinnments(request):
    app = Appointments.objects.select_related('patientID', 'doctorID').all()
    context = {
        'app': app,
    }
    return render(request, 'all_appointment.html', context)

@login_required(login_url="/admin/login/")
@staff_member_required
@csrf_exempt
def create_appointment(request):
    if request.method == 'POST':
        form = CreatAppointment(request.POST)
        if form.is_valid():
            if form.cleaned_data['patientID'].age == None:
                messages.error(request, 'سجل بيانات المريض اولا!')
            elif form.cleaned_data['doctorID'].specialization == None:
                messages.error(request, 'اكمل تسجيل بيانات الدكتور!')
            else:
                form.save()
                messages.success(request, 'تمت اضافة الموعد بنجاح')
            redirect('/appointment/create_appointment/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            redirect('/appointment/create_appointment/')
    else:
        form = CreatAppointment()
    return render(request, 'create_appintment.html', {'form': form})


@login_required(login_url="/admin/login/")
@staff_member_required
def delete_appointment(request, id):
    try:
        app = Appointments.objects.get(id=id)
        app.delete()
        messages.success(request, 'تم حذف الموعد بنجاح!')
    except Appointments.DoesNotExist:
        messages.error(request, 'لم يتم حذف الموعد المحدد!')
    return redirect('/appointment/all_appintments/')

@login_required(login_url="/admin/login/")
@staff_member_required
def update_appointment(request, id):
    app = Appointments.objects.get(id=id)
    
    if request.method == 'POST':
        form = UpdateAppointment(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الموعد بنجاح!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    
        return redirect('/appointment/update_appintment/')
    else:
        form = UpdateAppointment(instance=app)

    return render(request, 'update_appointment.html', {'form': form, 'id':id})