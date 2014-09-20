#from django.db import models
from django.contrib.gis.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from datetime import datetime, timedelta

"""
    Model for all events created
"""
class Event(models.Model):
    owner = models.ForeignKey(User, db_index = True)
    latlng = models.PointField(srid=4326)
    latitude = models.DecimalField(max_digits = 20, decimal_places = 14)
    longitude = models.DecimalField(max_digits = 20, decimal_places = 14)
    address = models.CharField(max_length = 150)
    description = models.TextField()
    title = models.CharField(max_length = 150)
    contact_phone = models.CharField(max_length = 45, null = True)
    contact_email = models.EmailField(null = True)
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField(null = True)
    created_on = models.DateTimeField(auto_now_add = True) 
    last_updated_on = models.DateTimeField(auto_now = True)
    expires = models.DateTimeField(default = datetime.now() + timedelta(days=365)) 
    photo_count = models.IntegerField()
    attendance_count = models.IntegerField()
    
    objects = models.GeoManager()

"""
    Form for the Event model
"""  
class EventForm(ModelForm):
    class Meta:
        model = Event
        
        # remove from exclude list as we implement more functionality
        exclude = ('owner', 
                   'latlng',
                   'address', 
                   'contact_phone', 
                   'contact_email',
                   'event_start_date' 
                   'event_end_date', 
                   'created_on', 
                   'updated_on'
                   'last_updated_on',
                   'expires',
                   'photo_count',
                   'attendance_count')

"""
    Model for photos uploaded for new events
"""
class EventPhoto(models.Model):
    event = models.ForeignKey(Event, db_index = True)
    name = models.CharField(max_length = 150)
    size = models.IntegerField()
    
    # use a type set for the photo type
    
    type = models.CharField(max_length = 75)
    hash_key = models.CharField(max_length = 255) 
    
    objects = models.GeoManager()

"""
    Lookup table model for the attendance for a particular event
"""
class Attendance(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User, db_index = True)
    going = models.BooleanField()
    confirmed_on = models.DateTimeField(default = datetime.now())
    
    objects = models.GeoManager()
    