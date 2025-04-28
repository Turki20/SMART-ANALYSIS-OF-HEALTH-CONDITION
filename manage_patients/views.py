from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

# Create your views here.

from users.models import CustomUser, AdminLog
from .models import Patient
from .forms import CreatePatient, UpdatePatient, UpdateUserForm

@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def all_pateints(request):
    users = CustomUser.objects.all()
    patients = Patient.objects.select_related('userID').all()
    context = {
        'users': patients,
    }
    return render(request, 'all_patients.html', context)


@csrf_exempt
@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def create_patient(request):
    if request.method == 'POST':
        form = CreatePatient(request.POST)
        if form.is_valid():
            userID = form.cleaned_data.get('userID')
            try:
                suser = Patient.objects.select_related('userID').get(userID=userID.id)
            except Patient.DoesNotExist:
                suser = None

            if suser == None:
                patient = form.save()
                patient.save()
                newLog = AdminLog(adminID=request.user, action=f'اضافة مريض : [{patient.userID.username}]')
                newLog.save()
                messages.success(request, 'تم اضافة المريض بنجاح')
            elif suser != None and suser.age == None:
                p = Patient.objects.get(id=suser.id)
                updatForm = CreatePatient(request.POST, instance=p)
                updatForm.save()
                newLog = AdminLog(adminID=request.user, action=f'اضافة مريض : [{suser.userID.username}]')
                newLog.save()
                messages.success(request, 'تم اضافة المريض بنجاح')
            else:
                messages.error(request, 'المريض مسجل بالفعل')
            return redirect('/patient/create_patient/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CreatePatient()
    context = {
        'form': form,
    }
    return render(request, 'create_patient.html', context)

@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def delete_patient(request, userID):
    patient = Patient.objects.select_related('userID').get(id=userID)
    patient.delete()
    newLog = AdminLog(adminID=request.user, action=f'حذف مريض : [{patient.userID.username}]')
    newLog.save()
    messages.success(request, 'تم حذف سجل المريض بنجاح!')
    return redirect('/patient/all_patients/')

@csrf_exempt
@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def update_patient(request, id):
    patient = Patient.objects.select_related('userID').get(id=id)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'formPatientData':
            form = UpdatePatient(request.POST, instance=patient)
            formUser = UpdateUserForm(instance=patient.userID)
            if form.is_valid():
                form.save()
                newLog = AdminLog(adminID=request.user, action=f'تحديث بيانات المريض : [{patient.userID.username}]')
                newLog.save()
                messages.success(request, 'تم تحديث بيانات المريض بنجاح')
                redirect('/patient/update_patient/')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                redirect('/patient/update_patient/')
                
        elif form_type == 'formUserData':
            form = UpdatePatient(instance=patient)
            formUser = UpdateUserForm(request.POST, instance=patient.userID)
            if formUser.is_valid():
                formUser.save()
                newLog = AdminLog(adminID=request.user, action=f'تحديث بيانات المريض : [{patient.userID.username}]')
                newLog.save()
                messages.success(request, 'تم تحديث بيانات المستحدم بنجاح')
                redirect('/patient/update_patient/')
            else:
                for field, errors in formUser.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                redirect('/patient/update_patient/')
    else:
        form = UpdatePatient(instance=patient)
        formUser = UpdateUserForm(instance=patient.userID)
    
    context = {
        'form': form,
        'formUser':formUser,
        'id': id,
    }
    return render(request, 'update_patient.html', context)
    