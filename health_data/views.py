from django.shortcuts import render, redirect, get_object_or_404
from .models import HealthData
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required(login_url="/user/login/")
@staff_member_required(login_url='/user/not-authorized/')
def healthdata_list(request):
    healthdata = HealthData.objects.all().order_by('-timestamp') 
    return render(request, 'healthdata_list.html', {'healthdata': healthdata})


@login_required(login_url="/user/login/")
@staff_member_required(login_url='/user/not-authorized/')
def delete_healthdata(request, pk):
    record = get_object_or_404(HealthData, pk=pk)
    record.delete()
    messages.success(request, "تم حذف السجل بنجاح.")
    return redirect('healthdata_list')
