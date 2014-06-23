from django.contrib.gis import admin
from Geo.models import EventPoint

# Register your models here.
admin.site.register(EventPoint, admin.GeoModelAdmin)