# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Event_Point'
        db.delete_table(u'Geo_event_point')


    def backwards(self, orm):
        # Adding model 'Event_Point'
        db.create_table(u'Geo_event_point', (
            ('event_id', self.gf('django.db.models.fields.IntegerField')()),
            ('latlng', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'Geo', ['Event_Point'])


    models = {
        
    }

    complete_apps = ['Geo']