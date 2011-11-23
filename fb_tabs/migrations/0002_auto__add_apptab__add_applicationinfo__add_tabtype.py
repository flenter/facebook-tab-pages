# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AppTab'
        db.create_table('fb_tabs_apptab', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publish_state', self.gf('django.db.models.fields.CharField')(default='published', max_length=50)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('app_info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fb_tabs.ApplicationInfo'])),
            ('tab_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fb_tabs.TabType'])),
        ))
        db.send_create_signal('fb_tabs', ['AppTab'])

        # Adding model 'ApplicationInfo'
        db.create_table('fb_tabs_applicationinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publish_state', self.gf('django.db.models.fields.CharField')(default='published', max_length=50)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('app_id', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('app_secret', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('fb_tabs', ['ApplicationInfo'])

        # Adding model 'TabType'
        db.create_table('fb_tabs_tabtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publish_state', self.gf('django.db.models.fields.CharField')(default='published', max_length=50)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('related_view', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('fb_tabs', ['TabType'])


    def backwards(self, orm):
        
        # Deleting model 'AppTab'
        db.delete_table('fb_tabs_apptab')

        # Deleting model 'ApplicationInfo'
        db.delete_table('fb_tabs_applicationinfo')

        # Deleting model 'TabType'
        db.delete_table('fb_tabs_tabtype')


    models = {
        'fb_tabs.applicationinfo': {
            'Meta': {'object_name': 'ApplicationInfo'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'app_secret': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'publish_state': ('django.db.models.fields.CharField', [], {'default': "'published'", 'max_length': '50'})
        },
        'fb_tabs.apptab': {
            'Meta': {'object_name': 'AppTab'},
            'app_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fb_tabs.ApplicationInfo']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'publish_state': ('django.db.models.fields.CharField', [], {'default': "'published'", 'max_length': '50'}),
            'tab_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fb_tabs.TabType']"})
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
