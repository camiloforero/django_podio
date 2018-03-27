# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-20 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_podio', '0014_auto_20160920_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='aplicacion',
            name='organization',
            field=models.CharField(help_text='The organization this application belongs to', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='aplicacion',
            name='workspace',
            field=models.CharField(help_text='Espacio de trabajo al cual pertenece esta aplicaci\xf3n', max_length=64),
        ),
    ]