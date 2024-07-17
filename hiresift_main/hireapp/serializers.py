from rest_framework import serializers
from .models import EmployeeForm

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=EmployeeForm
        fields = ['job_title','job_description','starting_date','ending_date']