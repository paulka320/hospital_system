from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """User profile with role management"""
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('doctor', 'Doctor'),
        ('receptionist', 'Receptionist'),
        ('lab_technician', 'Lab Technician'),
        ('accountant', 'Accountant'),
        ('patient', 'Patient'),
    )

    DEPARTMENT_CHOICES = (
        ('general', 'General'),
        ('cardiology', 'Cardiology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('gynecology', 'Gynecology'),
        ('neurology', 'Neurology'),
        ('psychiatry', 'Psychiatry'),
        ('emergency', 'Emergency'),
        ('icu', 'ICU'),
        ('reception', 'Reception'),
        ('laboratory', 'Laboratory'),
        ('billing', 'Billing'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='general', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='profile_images/default.png')
    bio = models.TextField(blank=True, null=True)
    is_active_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    @property
    def is_doctor(self):
        return self.role == 'doctor'

    @property
    def is_receptionist(self):
        return self.role == 'receptionist'

    @property
    def is_lab_technician(self):
        return self.role == 'lab_technician'

    @property
    def is_accountant(self):
        return self.role == 'accountant'

    @property
    def is_patient(self):
        return self.role == 'patient'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.user.is_superuser

    @property
    def display_name(self):
        return f"{self.user.first_name} {self.user.last_name}" if self.user.first_name else self.user.username

    @property
    def avatar_url(self):
        if self.profile_image:
            return self.profile_image.url
        return '/static/images/default-avatar.png'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a user profile when a new user is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Automatically save the user profile when the user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
