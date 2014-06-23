#from django.db import models
from django.contrib.gis.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

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
    event_date = models.DateTimeField()
    event_end_date = models.DateTimeField(null = True)
    
    # Should actually never be blank/NULL, only has that property for migrations
    created_on = models.DateTimeField(null = True, blank = True, auto_now_add = True) 
    updated_on = models.DateTimeField(null = True, blank = True, auto_now = True)
     
    # @todo: Add expires field to automatically remove an event after a certain time period
    # @note: This may or may not be represented by the event_end_date
    
    objects = models.GeoManager()

"""
    Form for the Event model
    
    @todo: Update this form to reflect the form in its current form
"""  
class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('owner', 'latlng', 'contact_phone', 'contact_email', 'event_end_date', 'created_on', 'updated_on')

"""
    Model for photos uploaded for new events
    
    @attention: The actual photos are stored in the server filesystem in
    the storage/photos folder
"""
class EventPhoto(models.Model):
    event = models.ForeignKey(Event, db_index = True)
    name = models.CharField(max_length = 150)
    size = models.IntegerField()
    
    # File type (extension), if blank assumed .txt?
    type = models.CharField(max_length = 75, null = True, blank = True)
    hash_key = models.CharField(max_length = 255) # Index on this field ?
    
    
    # @todo: Add any additional fields a photo stored for an event may need, or that may be of use
    # engineering wise
    