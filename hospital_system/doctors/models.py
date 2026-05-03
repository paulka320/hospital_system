from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.utils import timezone

# Create your models here.
class Doctor(models.Model):
    GENDER_CHOICES = [
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    license_number = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='doctors/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_patients = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['specialization']),
            models.Index(fields=['is_available']),
        ]

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"


class DoctorAvailability(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('doctor', 'day_of_week')
        verbose_name_plural = "Doctor Availabilities"
    
    def __str__(self):
        return f"Dr. {self.doctor.name} - {self.get_day_of_week_display()}"


class DoctorReview(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    patient = models.ForeignKey('patients.Patient', on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.doctor.name} - {self.rating} stars"