from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, AdminLog
from .forms import CreateUserForm, UpdateUserForm
from manage_patients.models import Patient
from django.contrib import messages
from manage_doctors.models import Doctor
from django.contrib.auth import logout

# Create your views here.

@csrf_exempt
@login_required(login_url="/admin/login/")
@staff_member_required
def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            role = form.cleaned_data.get('role')
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True 
            elif role == 'patient':
                newpatient = Patient(userID=user)
                newpatient.save()
            elif role == 'doctor':
                newDoctor = Doctor(userID=user)
                newDoctor.save()
                
            user.save()
            newLog = AdminLog(adminID=request.user, action=f'اضافة مستخدم جديد: [{user.username}]')
            newLog.save()
            messages.success(request, 'تم إنشاء المستخدم بنجاح')
            return redirect('/user/create_user/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CreateUserForm()
    context = {
        'form': form,
    }
    return render(request, 'create_user.html', context)

@login_required(login_url="/admin/login/")
@staff_member_required
def all_user(request):
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'all_users.html', context)

@login_required(login_url="/admin/login/")
@staff_member_required
def update_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            newLog = AdminLog(adminID=request.user, action=f'تم تحديث المستخدم: [{user.username}]')
            newLog.save()
            messages.success(request, 'تم تحديث المستخدم بنجاح!')
            return redirect(f'/user/update/{user_id}/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UpdateUserForm(instance=user)
    return render(request, 'update_user.html', {'form': form, 'user': user})

def delete_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    newLog = AdminLog(adminID=request.user, action=f'حذف مستخدم : [{user.username}]')
    newLog.save()
    messages.success(request, 'تم حذف المستخدم بنجاح!')
    return redirect('/user/all_users/')


def logout_view(request):
    logout(request) 
    return redirect('/') 