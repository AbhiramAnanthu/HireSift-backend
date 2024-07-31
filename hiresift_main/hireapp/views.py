from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EmployeeSerializer, ApplicantSerializer
from rest_framework import status
from .models import *
from .resume import extractor, prompting_storing
from django.http import FileResponse, HttpResponseNotFound, HttpResponse,JsonResponse
from tempfile import TemporaryDirectory
import uuid
import zipfile
import json


class JobView(APIView):
    def get(self, request):
        job = JobForm.objects.all()
        serializer = EmployeeSerializer(job, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            id = uuid.uuid4()
            instance = serializer.create(
                validated_data={**serializer.validated_data, "job_id": id}
            )
            instance.save()
            response_serializer=EmployeeSerializer(instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicantView(APIView):
    def get(self, request):
        id=request.query_params.get('job_id',None)
        applicant = ApplicantData.objects.filter(job_id=id)
        serializer = ApplicantSerializer(applicant, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ApplicantSerializer(data=request.data)
        if serializer.is_valid():
            id = uuid.uuid4()
            instance = serializer.create(
                validated_data={**serializer.validated_data, "application_number": id}
            )
            instance.save()
            response_serializer = ApplicantSerializer(instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class download_files(APIView):
    def get(self, request):
        id=request.query_params.get('applicant_number',None)
        applicants = ApplicantData.objects.filter(application_number=id)
        for applicant in applicants:
            file_name=applicant.get_file_name()
            dir='C:/Users/aaran/OneDrive/Desktop/HireSift-backend/hiresift_main/media/'
            file_path=os.path.join(dir,file_name)
            return FileResponse(open(file_path,'rb'),as_attachment=True,filename=file_name)
        
class LangView(APIView):
  def get(self, request):
    user_input=request.query_params.get('user_input',None)
    id=request.query_params.get('id',None)
    if not id:
        return HttpResponse("Error: 'id' parameter is required and cannot be empty.", status=400)

    data = passing_to_langchain(user_input, id)
    json_data = json.dumps(data)
    return HttpResponse(json_data)

class ApplicantDetails(APIView):
    def get(self,request):
        data=[]
        id=request.query_params.get('id',None)
        applicants = ApplicantData.objects.filter(application_number=id)
        for applicant in applicants:
            data.append({
                'id':applicant.application_number,
                'Name':applicant.__str__(),
                'phone':applicant.appl_phone,
                'email':applicant.appl_email,
            })
        return HttpResponse(data)

def passing_to_langchain(user_input,id):
    applicants = ApplicantData.objects.filter(job_id=id)
    all_docs = []
    document = []
    resume_pages = []
    for applicant in applicants:
        file_name = applicant.get_file_name()
        directory = (
            "C:/Users/aaran/OneDrive/Desktop/HireSift-backend/hiresift_main/media/"
        )
        file_path = os.path.join(directory, file_name)
        id = applicant.application_number
        docs = {"id": id, "file_path": file_path}
        all_docs.append(docs)
    for doc in all_docs:
        text = extractor(doc)
        document.append(text)
    for page in document:
        for i in page:
            resume_pages.append({"id": i.id, "page_content": i.page_content})
    result = prompting_storing(user_input, resume_pages)
    return result


def getting_sorted_files():
    files = []
    applicants = ApplicantData.objects.all()
    for applicant in applicants:
        file_name = applicant.get_file_name()
        dir = "C:/Users/aaran/OneDrive/Desktop/HireSift-backend/hiresift_main/media/"
        file_path = os.path.join(dir, file_name)
        files.append(file_path)
    return files
