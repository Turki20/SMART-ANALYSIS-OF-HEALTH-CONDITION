from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

# Create your views here.
from .models import Doctor, Specialty
from .forms import CreateDoctorForm, UpdateDoctorForm, UpdateUserForm
from users.models import AdminLog, CustomUser

@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def all_doctors(request):
    doctors = Doctor.objects.select_related('userID').all()
    context = {
        'doctors': doctors,
    }
    return render(request, 'all_doctors.html', context)


@csrf_exempt
@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def create_doctor(request):
    if request.method == 'POST':
        form = CreateDoctorForm(request.POST)
        if form.is_valid():
            userID = form.cleaned_data.get('userID')
            try:
                suser = Doctor.objects.select_related('userID').get(userID=userID.id)
            except Doctor.DoesNotExist:
                suser = None

            if suser == None:
                checkDoctor = CustomUser.objects.get(id=userID.id).role
                if checkDoctor != 'doctor':
                    messages.error(request, 'المستخدم ليس مسجل كدكتور! ')
                    return redirect('/doctor/create_doctor/')
                doctor = form.save()
                doctor.save()
                newLog = AdminLog(adminID=request.user, action=f'اضافة دكتور : [{doctor.userID.username}]')
                newLog.save()
                messages.success(request, 'تم اضافة الدكتور بنجاح')
            elif suser != None and suser.specialty == None:
                d = Doctor.objects.get(id=suser.id)
                updateDoctor = CreateDoctorForm(request.POST, instance=d)
                doctor = updateDoctor.save()
                doctor.save()
                newLog = AdminLog(adminID=request.user, action=f'اضافة دكتور : [{suser.userID.username}]')
                newLog.save()
                messages.success(request, 'تم اضافة الدكتور بنجاح')
            else:
                messages.error(request, 'الدكتور مسجل بالفعل')
            return redirect('/doctor/create_doctor/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CreateDoctorForm()
    context = {
        'form': form,
    }
    return render(request, 'create_doctor.html', context)

@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def delete_doctor(request, id):
    doctor = Doctor.objects.get(id=id)
    doctor.delete()
    newLog = AdminLog(adminID=request.user, action=f'حذف دكتور : [{doctor.userID.username}]')
    newLog.save()
    messages.success(request, 'تم حذف الدكتور بنجاح')
    return redirect('/doctor/all_doctors/')

@csrf_exempt
@login_required(login_url="/admin/login/")
@staff_member_required(login_url='/user/not-authorized/')
def update_doctor(request, id):
    doctor = Doctor.objects.select_related('userID').get(id=id)
    
    
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'formDoctorData':
            form = UpdateDoctorForm(request.POST, instance=doctor)
            formUser = UpdateUserForm(instance=doctor.userID)
            if form.is_valid():
                form.save()
                newLog = AdminLog(adminID=request.user, action=f'تحديث بيانات دكتور : [{doctor.userID.username}]')
                newLog.save()
                messages.success(request, 'تم تحديث بيانات الدكتور بنجاح')
                redirect('/doctor/update_doctor/')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                redirect('/doctor/update_doctor/')
                
        elif form_type == 'formUserData':
            form = UpdateDoctorForm(instance=doctor)
            formUser = UpdateUserForm(request.POST, instance=doctor.userID)
            if formUser.is_valid():
                formUser.save()
                newLog = AdminLog(adminID=request.user, action=f'تحديث بيانات دكتور : [{doctor.userID.username}]')
                newLog.save()
                messages.success(request, 'تم تحديث بيانات المستحدم بنجاح')
                redirect('/doctor/update_doctor/')
            else:
                for field, errors in formUser.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                redirect('/doctor/update_doctor/')
    else:
        form = UpdateDoctorForm(instance=doctor)
        formUser = UpdateUserForm(instance=doctor.userID)
    
    context = {
        'form': form,
        'formUser':formUser,
        'id': id,
    }
    return render(request, 'update_doctor.html', context)
    