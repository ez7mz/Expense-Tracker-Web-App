from datetime import date
from email.policy import default
from django.db import models

# Create your models here.

class Transaction(models.Model):
    CHOICES = (
        ('Housing', 'Housing'),
        ('School', 'School'),
        ('Transportation', 'Transportation'),
        ('Insurance', 'Insurance'),
        ('Medical', 'Medical'),
        ('Saving', 'Saving'),
    )
    Id = models.AutoField(auto_created = True, primary_key = True)
    title = models.CharField(max_length=20)
    date = models.DateField()
    Type = models.CharField(max_length=7)
    amount = models.FloatField(default=0)
    Category = models.CharField(max_length=30, choices = CHOICES, blank=True)
    username = models.CharField(max_length=20)

    def __str__(self):
        return self.username + " | " + self.title
    
    class Meta:
        ordering = ['-date']