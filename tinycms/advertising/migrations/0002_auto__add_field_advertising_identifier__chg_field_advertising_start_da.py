# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Advertising.identifier'
        db.add_column(u'advertising_advertising', 'identifier',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


        # Changing field 'Advertising.start_date'
        db.alter_column(u'advertising_advertising', 'start_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Advertising.identifier'
        db.delete_column(u'advertising_advertising', 'identifier')


        # Changing field 'Advertising.start_date'
        db.alter_column(u'advertising_advertising', 'start_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=''))

    models = {
        u'advertising.advertising': {
            'Meta': {'object_name': 'Advertising'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'advertising.media': {
            'Meta': {'object_name': 'Media'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['advertising']