from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EmployeeSerializer,ApplicantSerializer
from rest_framework import status
from .models import *
from .resume import extractor,prompting_storing
from django.http import JsonResponse
import uuid

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
    
class ApplicantView(APIView):
    def get(self,request):
        applicant=ApplicantData.objects.all()
        serializer=ApplicantSerializer(applicant,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=ApplicantSerializer(data=request.data)
        if serializer.is_valid():
            id=uuid.uuid4()
            instance=serializer.create(validated_data={**serializer.validated_data,"application_number":id})
            instance.save()
            response_serializer=ApplicantSerializer(instance)
            return Response(response_serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LangView(APIView):
    def get(self,request):
        data=passing_to_langchain()
        return Response(data)
    
def passing_to_langchain():
    applicants=ApplicantData.objects.all()
    all_docs=[]
    document=[]
    resume_pages=[]
    for applicant in applicants:
        file_name=applicant.get_file_name()
        directory="C:/Users/aaran/OneDrive/Desktop/HireSift-backend/hiresift_main/media/"
        file_path=os.path.join(directory,file_name)
        id=applicant.application_number
        docs={
            "id":id,
            "file_path":file_path
        }
        all_docs.append(docs)
    for doc in all_docs:
        text=extractor(doc)
        document.append(text)
    for page in document:
        for i in page:
            resume_pages.append({
                "id":i.id,
                "page_content":i.page_content
            })
    user_input="I want to hire a backend developer who knows any one of the language python,javascript,or ruby who knows deployment with docker."
    result=prompting_storing(user_input,resume_pages)
    return result