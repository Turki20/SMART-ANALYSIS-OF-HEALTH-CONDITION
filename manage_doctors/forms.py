from django import forms
from .models import Doctor
from users.models import CustomUser

class CreateDoctorForm(forms.ModelForm):
    availability = forms.CharField(required=True)
    class Meta:
        model = Doctor
        fields = ['userID', 'specialty', 'availability']
        
        
class UpdateDoctorForm(forms.ModelForm): # keep in minde update user data  -- 
    availability = forms.CharField(required=True)
    class Meta:
        model = Doctor
        fields = ['specialty', 'availability']
        
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        