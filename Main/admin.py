from django.contrib import admin
from Main.models import Event, EventPhoto, Attendance

# Register your models here.
admin.site.register(Event)
admin.site.register(EventPhoto)
admin.site.register(Attendance)