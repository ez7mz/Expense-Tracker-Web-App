from email.policy import default
from django.db import models

# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length=20)
    lname= models.CharField(max_length=20)
    profile = models.ImageField(upload_to='profiles', default='profiles/robot.png')
    username = models.CharField(max_length=8)
    password = models.CharField(max_length=12)
    balance = models.FloatField(default=1)
    income = models.FloatField(default=1)
    expense = models.FloatField(default=1)

    def __str__(self):
        return self.username