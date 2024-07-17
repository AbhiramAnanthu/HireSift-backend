from django.urls import path
from . import views

urlpatterns=[
    path('api/job-form',views.submit_form,name='job-form'),
]