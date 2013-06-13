# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'tinycms_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['tinycms.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('meta_extra', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'tinycms', ['Category'])

        # Adding model 'Symbol'
        db.create_table(u'tinycms_symbol', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'tinycms', ['Symbol'])

        # Adding model 'TitleClass'
        db.create_table(u'tinycms_titleclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_class', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'tinycms', ['TitleClass'])

        # Adding model 'EntryBase'
        db.create_table(u'tinycms_entrybase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entry_author', to=orm['auth.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='modified_by', null=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('alternate_title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('jump', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('jump_to_url', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50, blank=True)),
            ('category', self.gf('mptt.fields.TreeForeignKey')(related_name='entry_category', to=orm['tinycms.Category'])),
            ('source', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('alternate_thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1500, blank=True)),
            ('publish', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='entry_publisher', null=True, to=orm['auth.User'])),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('mod_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('allow_comment', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_draft', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('meta_extra', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('classname', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
        ))
        db.send_create_signal(u'tinycms', ['EntryBase'])

        # Adding M2M table for field titleclass on 'EntryBase'
        db.create_table(u'tinycms_entrybase_titleclass', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entrybase', models.ForeignKey(orm[u'tinycms.entrybase'], null=False)),
            ('titleclass', models.ForeignKey(orm[u'tinycms.titleclass'], null=False))
        ))
        db.create_unique(u'tinycms_entrybase_titleclass', ['entrybase_id', 'titleclass_id'])

        # Adding M2M table for field sub_category on 'EntryBase'
        db.create_table(u'tinycms_entrybase_sub_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entrybase', models.ForeignKey(orm[u'tinycms.entrybase'], null=False)),
            ('category', models.ForeignKey(orm[u'tinycms.category'], null=False))
        ))
        db.create_unique(u'tinycms_entrybase_sub_category', ['entrybase_id', 'category_id'])

        # Adding M2M table for field symbol on 'EntryBase'
        db.create_table(u'tinycms_entrybase_symbol', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entrybase', models.ForeignKey(orm[u'tinycms.entrybase'], null=False)),
            ('symbol', models.ForeignKey(orm[u'tinycms.symbol'], null=False))
        ))
        db.create_unique(u'tinycms_entrybase_symbol', ['entrybase_id', 'symbol_id'])

        # Adding model 'Article'
        db.create_table(u'tinycms_article', (
            (u'entrybase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tinycms.EntryBase'], unique=True, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'tinycms', ['Article'])

        # Adding model 'Video'
        db.create_table(u'tinycms_video', (
            (u'entrybase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tinycms.EntryBase'], unique=True, primary_key=True)),
            ('video_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'tinycms', ['Video'])

        # Adding model 'Hit'
        db.create_table(u'tinycms_hit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tinycms.EntryBase'], unique=True)),
            ('hit', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'tinycms', ['Hit'])

        # Adding model 'Media'
        db.create_table(u'tinycms_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('upload_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'tinycms', ['Media'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'tinycms_category')

        # Deleting model 'Symbol'
        db.delete_table(u'tinycms_symbol')

        # Deleting model 'TitleClass'
        db.delete_table(u'tinycms_titleclass')

        # Deleting model 'EntryBase'
        db.delete_table(u'tinycms_entrybase')

        # Removing M2M table for field titleclass on 'EntryBase'
        db.delete_table('tinycms_entrybase_titleclass')

        # Removing M2M table for field sub_category on 'EntryBase'
        db.delete_table('tinycms_entrybase_sub_category')

        # Removing M2M table for field symbol on 'EntryBase'
        db.delete_table('tinycms_entrybase_symbol')

        # Deleting model 'Article'
        db.delete_table(u'tinycms_article')

        # Deleting model 'Video'
        db.delete_table(u'tinycms_video')

        # Deleting model 'Hit'
        db.delete_table(u'tinycms_hit')

        # Deleting model 'Media'
        db.delete_table(u'tinycms_media')


    models = {
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tinycms.article': {
            'Meta': {'ordering': "['-pub_date', '-id']", 'object_name': 'Article', '_ormbases': [u'tinycms.EntryBase']},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'entrybase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tinycms.EntryBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'tinycms.category': {
            'Meta': {'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_extra': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['tinycms.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'tinycms.entrybase': {
            'Meta': {'ordering': "['-pub_date', '-id']", 'object_name': 'EntryBase'},
            'allow_comment': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alternate_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'alternate_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entry_author'", 'to': u"orm['auth.User']"}),
            'category': ('mptt.fields.TreeForeignKey', [], {'related_name': "'entry_category'", 'to': u"orm['tinycms.Category']"}),
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jump': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jump_to_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'meta_extra': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'mod_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'modified_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'entry_publisher'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'sub_category': ('mptt.fields.TreeManyToManyField', [], {'blank': 'True', 'related_name': "'sub_category'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tinycms.Category']"}),
            'symbol': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['tinycms.Symbol']", 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'titleclass': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['tinycms.TitleClass']", 'null': 'True', 'blank': 'True'})
        },
        u'tinycms.hit': {
            'Meta': {'object_name': 'Hit'},
            'entry': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tinycms.EntryBase']", 'unique': 'True'}),
            'hit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tinycms.media': {
            'Meta': {'object_name': 'Media'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'upload_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'tinycms.symbol': {
            'Meta': {'object_name': 'Symbol'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'tinycms.titleclass': {
            'Meta': {'object_name': 'TitleClass'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_class': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'tinycms.video': {
            'Meta': {'ordering': "['-pub_date', '-id']", 'object_name': 'Video', '_ormbases': [u'tinycms.EntryBase']},
            u'entrybase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tinycms.EntryBase']", 'unique': 'True', 'primary_key': 'True'}),
            'video_url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['tinycms']