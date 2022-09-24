from django.db import models

# Create your models here.
class AnlyseFile(models.Model):
    file = models.FileField(upload_to='Files_to_Analyse')