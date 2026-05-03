from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('appointment_reminder', 'Appointment Reminder'),
        ('appointment_confirmed', 'Appointment Confirmed'),
        ('appointment_cancelled', 'Appointment Cancelled'),
        ('lab_result_ready', 'Lab Result Ready'),
        ('prescription_filled', 'Prescription Filled'),
        ('bill_issued', 'Bill Issued'),
        ('payment_received', 'Payment Received'),
        ('general', 'General Notification'),
    ]
    
    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPE_CHOICES
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Link to related objects
    content_type = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    object_id = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class NotificationPreference(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preference'
    )
    
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    
    # Notification preferences
    appointment_reminders = models.BooleanField(default=True)
    lab_results = models.BooleanField(default=True)
    billing_alerts = models.BooleanField(default=True)
    prescription_alerts = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Preferences for {self.user.username}"
