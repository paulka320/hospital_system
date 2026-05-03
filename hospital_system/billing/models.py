from django.db import models
from patients.models import Patient
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class Bill(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('check', 'Check'),
        ('online', 'Online Transfer'),
        ('insurance', 'Insurance'),
    ]
    
    bill_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='bills'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    issued_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        null=True,
        blank=True
    )
    
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient', 'status']),
            models.Index(fields=['bill_number']),
        ]

    def __str__(self):
        return f"Bill {self.bill_number} - {self.patient.name}"
    
    def save(self, *args, **kwargs):
        # Calculate total
        self.subtotal = sum(item.get_total() for item in self.items.all())
        self.total_amount = self.subtotal + self.tax - self.discount
        super().save(*args, **kwargs)
    
    def mark_paid(self, amount=None, payment_method='cash'):
        """Mark bill as paid"""
        if amount is None:
            amount = self.total_amount
        self.paid_amount = amount
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.payment_method = payment_method
        self.save()


class BillItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('procedure', 'Procedure'),
        ('medicine', 'Medicine'),
        ('lab_test', 'Laboratory Test'),
        ('room_charge', 'Room Charge'),
        ('other', 'Other'),
    ]
    
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPE_CHOICES,
        default='other'
    )
    
    description = models.CharField(max_length=255)
    
    quantity = models.IntegerField(default=1)
    
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    notes = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return self.quantity * self.unit_price
    
    def subtotal(self):
        return self.get_total()
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.description} - {self.get_total()}"


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    payment_method = models.CharField(
        max_length=20,
        choices=Bill.PAYMENT_METHOD_CHOICES
    )
    
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.id} - {self.amount} ({self.status})"