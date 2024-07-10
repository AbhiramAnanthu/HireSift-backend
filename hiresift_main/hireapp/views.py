from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ApplicantData
from .resume import  scanning,filtering
from .forms import ApplicantForm
import os
import uuid

def main(request):
    result = ranking()
    return render(request, "result.html", {"result": result})

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


def ranking():
    results = documentation()
    rank_container=[]
    for result in results:
        rank = filtering(result)
        rank_container.append(rank)
    return rank_container