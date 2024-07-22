# serializers.py
from rest_framework import serializers
from .models import JobForm, ApplicantData

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobForm
        fields = ['job_title', 'job_description', 'starting_date', 'ending_date']
    
class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantData  # Corrected here
        fields = ['first_name', 'last_name', 'resume', 'appl_email', 'appl_phone','application_number']


    