from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    owner = models.ForeignKey(User, db_index = True)
    latitude = models.DecimalField(max_digits = 20, decimal_places = 14, db_index = True)
    longitude = models.DecimalField(max_digits = 20, decimal_places = 14, db_index = True)
    address = models.CharField(max_length = 150)
    description = models.TextField()
    title = models.CharField(max_length = 150)
    contact_phone = models.CharField(max_length = 45)
    contact_email = models.EmailField()
    event_startdate = models.DateTimeField()
    event_enddate = models.DateTimeField()