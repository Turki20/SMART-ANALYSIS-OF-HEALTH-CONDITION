from django import forms
from .models import Appointments

class CreatAppointment(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ['patientID', 'doctorID', 'status', 'time'] 
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'patientID': forms.Select(attrs={'class': 'form-control'}),
            'doctorID': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(CreatAppointment, self).__init__(*args, **kwargs)
        self.fields['patientID'].required = False
        
class UpdateAppointment(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ['patientID', 'doctorID', 'status', 'time'] 
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'patientID': forms.Select(attrs={'class': 'form-control'}),
            'doctorID': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(UpdateAppointment, self).__init__(*args, **kwargs)
        self.fields['patientID'].required = False