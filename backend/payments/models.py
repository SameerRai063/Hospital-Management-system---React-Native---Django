from django.db import models
from users.models import Patient
from appointments.models import Appointment
# Create your models here.
class Payment(models.Model):

    GATEWAY_CHOICES = [
        ("khalti", "Khalti"),
    ]

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    gateway = models.CharField(
        max_length=20,
        choices=GATEWAY_CHOICES
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    paid_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.transaction_id}"