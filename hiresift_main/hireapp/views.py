from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EmployeeSerializer
from rest_framework import status
from .models import *

class JobView(APIView):
    def get(self,request):
        job=JobForm.objects.all()
        serializer=EmployeeSerializer(job,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        print(request.data)
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
