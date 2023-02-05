from django import forms
from .models import *

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ('status', 'user', 'dob')