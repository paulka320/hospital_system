from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    GENDER_CHOICES =[
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    ]
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    chronic_diseases = models.TextField(null=True, blank=True)
    insurance_provider = models.CharField(max_length=100, null=True, blank=True)
    insurance_id = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['phone']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.id})"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True, related_name='medical_records')
    diagnosis = models.TextField()
    disease = models.CharField(max_length=255)
    prescription = models.TextField()
    visit_date = models.DateField(auto_now_add=True)
    review_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-visit_date']
        indexes = [
            models.Index(fields=['patient', 'visit_date']),
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.disease}"
    
class Visit(models.Model):
    STATUS_CHOICES =[
        ('scheduled', 'Scheduled'),
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='visits')
    visit_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(null=True, blank=True)
    vitals = models.TextField(null=True, blank=True)  # Blood pressure, temperature, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-visit_date']
        indexes = [
            models.Index(fields=['patient', 'status']),
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.status} ({self.visit_date})"

class Laboratory(models.Model):
    TEST_CHOICES = [
        ('blood', 'Blood Test'),
        ('malaria', 'Malaria Test'),
        ('covid', 'COVID-19 Test'),
        ('urine', 'Urine Test'),
        ('xray', 'X-Ray'),
        ('ultrasound', 'Ultrasound'),
        ('ct_scan', 'CT Scan'),
        ('ecg', 'ECG'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='laboratory_tests')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True, related_name='laboratory_tests')
    visit = models.ForeignKey('patients.Visit', on_delete=models.CASCADE, null=True, blank=True)
    test_type = models.CharField(max_length=50, choices=TEST_CHOICES)
    result = models.TextField(blank=True)
    requested_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    technician_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-requested_date']
        indexes = [
            models.Index(fields=['patient', 'completed']),
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.test_type}"


class Prescription(models.Model):
    DOSAGE_UNIT_CHOICES = [
        ('mg', 'Milligram'),
        ('ml', 'Milliliter'),
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('injection', 'Injection'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('filled', 'Filled'),
    ]
    
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True, related_name='prescriptions')
    
    medicine_name = models.CharField(max_length=255)
    dosage = models.IntegerField()
    dosage_unit = models.CharField(max_length=20, choices=DOSAGE_UNIT_CHOICES)
    frequency = models.CharField(max_length=100)  # e.g., "3 times a day"
    duration_days = models.IntegerField()
    instructions = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    filled_at = models.DateTimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient', 'status']),
        ]
    
    def __str__(self):
        return f"{self.medicine_name} for {self.patient.name}"