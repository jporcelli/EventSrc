# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event_Point'
        db.create_table(u'Geo_event_point', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latlng', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('event_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Geo', ['Event_Point'])


    def backwards(self, orm):
        # Deleting model 'Event_Point'
        db.delete_table(u'Geo_event_point')


    models = {
        u'Geo.event_point': {
            'Meta': {'object_name': 'Event_Point'},
            'event_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlng': ('django.contrib.gis.db.models.fields.PointField', [], {})
        }
    }

    complete_apps = ['Geo']