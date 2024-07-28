from django.db import models
from django.utils import timezone
import os

class JobForm(models.Model):
    job_id=models.CharField(max_length=20,null=True,unique=True)
    job_title = models.CharField(max_length=255, null=False, blank=True)
    job_description = models.TextField()
    starting_date = models.DateField(default=timezone.now)
    ending_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.job_title
    
class ApplicantData(models.Model):
    application_number = models.CharField(max_length=20, null=True, unique=True)
    first_name = models.CharField(max_length=100, help_text="Enter your first name")
    last_name = models.CharField(max_length=100, help_text="Enter the last name")
    resume = models.FileField()
    upload_time = models.DateTimeField(auto_now_add=True, null=True)
    appl_email = models.EmailField()
    appl_phone = models.CharField(max_length=15)
    appl_essay = models.TextField(null=True)
    address=models.CharField(max_length=200,null=True)
    job_id=models.CharField(max_length=200,null=True)

    def get_file_name(self):
        return os.path.basename(self.resume.name)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



    