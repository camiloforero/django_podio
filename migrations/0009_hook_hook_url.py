# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-22 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_podio', '0008_auto_20160331_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='hook',
            name='hook_url',
            field=models.CharField(default='undefined', max_length=128),
            preserve_default=False,
        ),
    ]