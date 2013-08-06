# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Advertising.adv_title'
        db.add_column(u'advertising_advertising', 'adv_title',
                      self.gf('django.db.models.fields.CharField')(default='tmp', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Advertising.adv_title'
        db.delete_column(u'advertising_advertising', 'adv_title')


    models = {
        u'advertising.advertising': {
            'Meta': {'object_name': 'Advertising'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'adv_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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