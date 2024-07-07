from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ApplicantData
from .resume import document_loader, scanning, vector, vector_search
from .forms import ApplicantForm


def main(request):
    result=searching()
    return render(request, "result.html", {"result": result})

def vector_storing():
    content=documentation()
    id=content.get('id')
    result=content.get('result')
    document=[]
    document.append(vector(id,result))
    return {
        "document":document,
        "id":id,
        "file_path":content.get('file_path')
    }

def searching():
    loader=vector_storing()
    document=loader['document']
    id=loader['id']
    file_path=loader['file_path']
    search_results=vector_search(document,file_path)
    return search_results

def formSubmition(request):
    if request.method == "POST":
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success")

    else:
        form = ApplicantForm()

    return render(request, "upload_resume.html", {"form": form})


def documentation():
    applicants = ApplicantData.objects.all()
    content = {}
    for applicant in applicants:
        file_name = applicant.get_file_name()
        file_path = f"C:/Users/aaran/OneDrive/Desktop/HireSift-backend/hiresift_main/media/{file_name}"
        loader=scanning(file_path)
        content.update({"id": applicant.application_number, "file_path": file_path,'result':loader["result"]})
    return content

