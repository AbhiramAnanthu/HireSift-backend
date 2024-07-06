from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ApplicantData
from .resume import document_loader,scanning
from .forms import ApplicantForm

def main(request):
    content=documentation()
    file_path=content.get('file_path')
    result=scanning(file_path)
    return render(request,'result.html',{'result':result})

def formSubmition(request):
    if request.method == 'POST':
        form = ApplicantForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
            
    else:
        form = ApplicantForm()

    return render(request, 'upload_resume.html', {'form': form})
    
def documentation():
    applicants=ApplicantData.objects.all()
    content={}
    for applicant in applicants:
        file_name=applicant.get_file_name()
        file_path=f"C:/Users/aaran/OneDrive/Desktop/HireSift-backend/hiresift_main/media/{file_name}"
        content.update({"id":applicant.application_number,"file_path":file_path})
    return content