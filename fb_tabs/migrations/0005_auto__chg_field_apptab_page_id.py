# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'AppTab.page_id'
        db.alter_column('fb_tabs_apptab', 'page_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))


    def backwards(self, orm):
        
        # Changing field 'AppTab.page_id'
        db.alter_column('fb_tabs_apptab', 'page_id', self.gf('django.db.models.fields.CharField')(default='0', max_length=100))


    models = {
        'fb_tabs.applicationinfo': {
            'Meta': {'object_name': 'ApplicationInfo'},
            'app_id': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '25'}),
            'app_secret': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '100'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'publish_state': ('django.db.models.fields.CharField', [], {'default': "'published'", 'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fb_tabs.apptab': {
            'Meta': {'object_name': 'AppTab'},
            'app_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fb_tabs.ApplicationInfo']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'publish_state': ('django.db.models.fields.CharField', [], {'default': "'published'", 'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tab_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fb_tabs.TabType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fb_tabs.tabtype': {
            'Meta': {'object_name': 'TabType'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'publish_state': ('django.db.models.fields.CharField', [], {'default': "'published'", 'max_length': '50'}),
            'related_view': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['fb_tabs']
