from django.db import models

# Create your models here.
class Patient(models.Model):
    GENDER_CHOICES =[
        ('M','Male'),
        ('F','Female'),
    ]
    name = models.CharField(max_length =100)
    age =models.IntegerField()
    gender =models.CharField(max_length=1,choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor',on_delete=models.SET_NULL,null=True)
    diagnosis = models.TextField()
    disease = models.CharField(max_length=255)
    prescription = models.TextField()
    visit_date = models.DateField(auto_now_add=True)
    review_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return f"{self.patient.name}-{self.disease}"
    
class Visit(models.Model):
    STATUS_CHOICES =[
        ('waiting','Waiting'),
        ('in_progress','In progress'),
        ('completed','Completed'),
    ]
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor',on_delete=models.SET_NULL,null=True,blank=True)
    visit_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20,choices = STATUS_CHOICES,default='Waiting')

    def __str__(self):
        return f"{self.patient}-{self.status}"

class Laboratory(models.Model):
    TEST_CHOICES = [
        ('blood','Blood Test'),
        ('malaria','Malaria Test'),
        ('covid','COVID-19 Test'),
        ('urine','Urine Test'),
    ]
    patient = models.ForeignKey(Patient,on_delete =models.CASCADE)
    doctor =models.ForeignKey('doctors.Doctor',on_delete=models.SET_NULL,null=True)
    visit = models.ForeignKey('patients.Visit',on_delete=models.CASCADE,null=True,blank=True)
    test_type = models.CharField(max_length=50,choices = TEST_CHOICES)
    result = models.TextField(blank=True)
    requested_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient}-{self.test_type}"