from django import forms
from .models import ApplicantData

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = ApplicantData
        fields = ["first_name", "last_name", "appl_email", "appl_phone", "resume"]
