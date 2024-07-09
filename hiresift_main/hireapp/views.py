from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ApplicantData
from .resume import document_loader, scanning, vector, vector_search
from .forms import ApplicantForm
import os
import uuid

def main(request):
    result = searching()
    return render(request, "result.html", {"result": result})


def vector_storing():
    data=[]
    document=[]
    applicants = documentation()
    for applicant in applicants:
        id = applicant.get("id")
        result = applicant.get("result")
        document.append(vector(result))
        resume_data = {
            "document":document,
            "id":id,
            "file_path":applicant.get('file_path')
        }
        data.append(resume_data)
    return data


def searching():
    data = vector_storing()
    search_results=[]
    for doc in data:
        document = doc.get("document")
        file_path = doc.get("file_path")
        search_results.append(vector_search(document, file_path))
    return search_results

def generate_application_number():
    return str(uuid.uuid4()).replace('-', '').upper()[:10]

def formSubmition(request):
    if request.method == "POST":
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            applicant=form.save(commit=False)
            application_number=generate_application_number()
            applicant.application_number = application_number
            applicant.save()

            return redirect("success",application_number=application_number)

    else: 
        form = ApplicantForm()

    return render(request, "upload_resume.html", {"form": form})


def documentation():
    applicants = ApplicantData.objects.all()
    content = []
    for applicant in applicants:
        file_name = applicant.get_file_name()
        file_path = os.path.join(
            "C:/Users/aaran/OneDrive/Desktop/HireSift-backend/hiresift_main/media",
            file_name,
        )
        loader = scanning(file_path)
        dict={
            "file_path": file_path,
            "result": loader["result"],
            "id":applicant.application_number
        }
        content.append(dict)

    return content

