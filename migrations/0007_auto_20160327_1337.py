# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-27 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_podio', '0006_hook_uses'),
    ]

    operations = [
        migrations.AddField(
            model_name='aplicacion',
            name='workspace',
            field=models.CharField(default='Undefined', max_length=32, verbose_name=b'Espacio de trabajo al cual pertenece esta aplicaci\xc3\xb3n'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aplicacion',
            name='nombre',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
