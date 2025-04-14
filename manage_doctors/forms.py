from django import forms
from .models import Doctor
from users.models import CustomUser

class CreateDoctorForm(forms.ModelForm):
    specialization = forms.CharField(required=True)
    availability = forms.CharField(required=True)
    class Meta:
        model = Doctor
        fields = ['userID', 'specialization', 'availability']
        
        
class UpdateDoctorForm(forms.ModelForm): # keep in minde update user data  -- 
    specialization = forms.CharField(required=True)
    availability = forms.CharField(required=True)
    class Meta:
        model = Doctor
        fields = ['specialization', 'availability']
        
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        