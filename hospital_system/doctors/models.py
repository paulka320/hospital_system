from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    GENDER_CHOICES = [
        ('M','Male'),
        ('F','Female'),
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)

    def __str__(self):
        return self.name