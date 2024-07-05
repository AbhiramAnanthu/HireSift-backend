from django.db import models

class Resume(models.Model):
    resume_file=models.FileField(upload_to="documents")
    upload_time=models.DateTimeField(auto_now_add=True)
