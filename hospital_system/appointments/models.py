from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('surgery', 'Surgery'),
        ('emergency', 'Emergency'),
        ('routine_check', 'Routine Check'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_reason = models.TextField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['date', 'time']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['status']),
            models.Index(fields=['doctor', 'date']),
        ]
        unique_together = ('doctor', 'patient', 'date', 'time')

    def __str__(self):
        return f"Appointment - {self.patient.name} with Dr. {self.doctor.name} on {self.date} at {self.time}"
    
    def is_upcoming(self):
        """Check if appointment is upcoming"""
        from datetime import datetime
        appointment_datetime = datetime.combine(self.date, self.time)
        return appointment_datetime > timezone.now() and self.status not in ['cancelled', 'completed']
    
    def is_today(self):
        """Check if appointment is today"""
        return self.date == timezone.now().date()
    
    def send_reminder(self):
        """Send appointment reminder to patient"""
        pass  # TODO: Implement reminder notification system