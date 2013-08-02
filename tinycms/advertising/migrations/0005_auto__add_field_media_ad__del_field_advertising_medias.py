# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Media.ad'
        db.add_column(u'advertising_media', 'ad',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ad_medias', to=orm['advertising.Advertising']),
                      keep_default=False)

        # Deleting field 'Advertising.medias'
        db.delete_column(u'advertising_advertising', 'medias_id')


    def backwards(self, orm):
        # Deleting field 'Media.ad'
        db.delete_column(u'advertising_media', 'ad_id')

        # Adding field 'Advertising.medias'
        db.add_column(u'advertising_advertising', 'medias',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='ad_medias', to=orm['advertising.Media']),
                      keep_default=False)


    models = {
        u'advertising.advertising': {
            'Meta': {'object_name': 'Advertising'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'advertising.media': {
            'Meta': {'object_name': 'Media'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ad_medias'", 'to': u"orm['advertising.Advertising']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['advertising']