# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'AppTab.title'
        db.add_column('fb_tabs_apptab', 'title', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)

        # Adding field 'ApplicationInfo.title'
        db.add_column('fb_tabs_applicationinfo', 'title', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'AppTab.title'
        db.delete_column('fb_tabs_apptab', 'title')

        # Deleting field 'ApplicationInfo.title'
        db.delete_column('fb_tabs_applicationinfo', 'title')


    models = {
        'fb_tabs.applicationinfo': {
            'Meta': {'object_name': 'ApplicationInfo'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'app_secret': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'page_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
