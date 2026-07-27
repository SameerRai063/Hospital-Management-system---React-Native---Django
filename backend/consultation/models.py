from django.db import models

from users.models import Doctor, Patient


class Consultation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='consultations')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    medicines = models.JSONField(default=list, blank=True)
    timing = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Consultation {self.id} - Doctor: {self.doctor} | Patient: {self.patient}"


