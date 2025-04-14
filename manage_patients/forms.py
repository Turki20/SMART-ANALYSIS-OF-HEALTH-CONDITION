from django.forms import ModelForm
from django import forms
from .models import Patient
from users.models import CustomUser


class CreatePatient(ModelForm):
    age = forms.IntegerField(required=True)
    gender = forms.CharField(required=True)
    class Meta:
        model = Patient
        fields = ['userID', 'age', 'gender', 'healthdataa']
        
class UpdatePatient(ModelForm): # keep in minde update user data  -- 
    age = forms.IntegerField(required=True)
    gender = forms.CharField(required=True)
    class Meta:
        model = Patient
        fields = ['age', 'gender', 'healthdataa']
        
class UpdateUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        