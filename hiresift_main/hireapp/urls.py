from django.urls import path
from . import views

urlpatterns=[
    path('candidates/',views.ApplicantView.as_view()),
    path('jobs/',views.JobView.as_view()),
    path('working/',views.LangView.as_view()),
    path('download-files/',views.download_files.as_view()),
]