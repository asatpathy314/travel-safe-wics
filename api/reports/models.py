from django.db import models

class Country(models.Model):
    name = models.TextField()
    criminality_index = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    travel_safety_report = models.TextField(null=True)
    health_report = models.TextField(null=True)  # Integrated field
    vaccines = models.TextField(null=True)
    diseases = models.TextField(null=True)
