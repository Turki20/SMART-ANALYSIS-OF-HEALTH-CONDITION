from django.contrib import admin
from .models import CustomUser, AdminLog
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(AdminLog)