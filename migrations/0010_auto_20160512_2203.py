# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 22:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_podio', '0009_hook_hook_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hook',
            old_name='name',
            new_name='path',
        ),
    ]
