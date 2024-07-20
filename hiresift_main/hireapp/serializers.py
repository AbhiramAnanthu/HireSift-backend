from rest_framework import serializers
from .models import JobForm

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=JobForm
        fields = ['job_title','job_description','starting_date','ending_date']