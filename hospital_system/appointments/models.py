from django.db import models
from patients.models import Patient
from doctors.models import Doctor
# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(Patient,on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor,on_delete = models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    notes=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.patient}-{self.doctor}"