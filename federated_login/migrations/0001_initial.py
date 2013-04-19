# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Association'
        db.create_table('federated_login_association', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('issued', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('lifetime', self.gf('django.db.models.fields.IntegerField')()),
            ('assoc_type', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('federated_login', ['Association'])

        # Adding unique constraint on 'Association', fields ['server_url', 'handle']
        db.create_unique('federated_login_association', ['server_url', 'handle'])

        # Adding model 'Nonce'
        db.create_table('federated_login_nonce', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('salt', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('federated_login', ['Nonce'])

        # Adding unique constraint on 'Nonce', fields ['server_url', 'timestamp', 'salt']
        db.create_unique('federated_login_nonce', ['server_url', 'timestamp', 'salt'])


    def backwards(self, orm):
        # Removing unique constraint on 'Nonce', fields ['server_url', 'timestamp', 'salt']
        db.delete_unique('federated_login_nonce', ['server_url', 'timestamp', 'salt'])

        # Removing unique constraint on 'Association', fields ['server_url', 'handle']
        db.delete_unique('federated_login_association', ['server_url', 'handle'])

        # Deleting model 'Association'
        db.delete_table('federated_login_association')

        # Deleting model 'Nonce'
        db.delete_table('federated_login_nonce')


    models = {
        'federated_login.association': {
            'Meta': {'unique_together': "(('server_url', 'handle'),)", 'object_name': 'Association'},
            'assoc_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'lifetime': ('django.db.models.fields.IntegerField', [], {}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'server_url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'federated_login.nonce': {
            'Meta': {'unique_together': "(('server_url', 'timestamp', 'salt'),)", 'object_name': 'Nonce'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'server_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['federated_login']