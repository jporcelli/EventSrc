# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'Main_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=14)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=14)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=45, null=True)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('event_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_end_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'Main', ['Event'])

        # Adding model 'EventPhoto'
        db.create_table(u'Main_eventphoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Main.Event'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('hash_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'Main', ['EventPhoto'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'Main_event')

        # Deleting model 'EventPhoto'
        db.delete_table(u'Main_eventphoto')


    models = {
        u'Main.event': {
            'Meta': {'object_name': 'Event'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {}),
            'event_end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '14'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '14'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'Main.eventphoto': {
            'Meta': {'object_name': 'EventPhoto'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Main.Event']"}),
            'hash_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Main']