from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class Event(models.Model):
    owner = models.ForeignKey(User, db_index = True)
    latitude = models.DecimalField(max_digits = 20, decimal_places = 14, db_index = True)
    longitude = models.DecimalField(max_digits = 20, decimal_places = 14, db_index = True)
    address = models.CharField(max_length = 150)
    description = models.TextField()
    title = models.CharField(max_length = 150)
    contact_phone = models.CharField(max_length = 45, null=True)
    contact_email = models.EmailField(null=True)
    event_date = models.DateTimeField()
    event_end_date = models.DateTimeField(null=True)
    
class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('owner', 'contact_phone', 'contact_email', 'event_end_date')