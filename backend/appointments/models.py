import uuid

from django.db import models

from users.models import Doctor, Patient


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )

    appointment_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    appointment_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            self.appointment_id = f"APT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-appointment_date']

    def __str__(self):
        return (
            f"{self.appointment_id} - "
            f"Doctor: {self.doctor} | Patient: {self.patient}"
        )