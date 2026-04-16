from django.db import models

# Create your models here.
from django.db import models
from patients.models import Patient


class Bill(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    paid = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"Bill {self.id} - {self.patient}"


class BillItem(models.Model):

    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name='items'
    )

    description = models.CharField(
        max_length=255
    )

    quantity = models.IntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):
        return self.quantity * self.price