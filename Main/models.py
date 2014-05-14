from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    owner = models.ForeignKey(User)
    latitude = models.DecimalField(max_digits=20, decimal_places=14)
    longitude = models.FloatField(max_digits=20, decimal_places=14)
    address = models.CharField()
    description = models.CharField()
    title = models.CharField()
    contact_phone = models.CharField()
    contact_email = models.EmailField()
    event_date = models.DateTimeField()
    event_end_date = models.DateTimeField()