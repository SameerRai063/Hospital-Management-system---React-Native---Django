from django.db import models
from users.models import Doctor, Patient
from appointments.models import Appointment
# Create your models here.
class Payment(models.Model):

    GATEWAY_CHOICES = [
        ("esewa", "Esewa"),
    ]

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="payment"
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
        return self.transaction_id
class PendingPayment(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="pending_payments"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="pending_payments"
    )

    appointment_date = models.DateTimeField()

    gateway_reference = models.CharField(
    max_length=100,
    unique=True,
    blank=True,
    null=True
)
    transaction_uuid = models.UUIDField(
    unique=True
)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient} -> {self.doctor}"