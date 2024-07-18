from rest_framework import serializers
from .models import EmployeeForm

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=EmployeeForm
        fields = '__all__'