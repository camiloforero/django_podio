# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_podio', '0011_auto_20160512_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aplicacion',
            name='workspace',
            field=models.CharField(help_text='Espacio de trabajo al cual pertenece esta aplicaci\xf3n', max_length=32),
        ),
        migrations.AlterField(
            model_name='hook',
            name='field',
            field=models.CharField(blank=True, help_text='If empty, this will be an app hook. If not, it will be an app_field hook. One main difference is that with an item.update trigger, the frist one will be triggered every time anything is modified, while the second will trigger only when the specific field is modificed', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='hook',
            name='label',
            field=models.CharField(help_text='A human readable name', max_length=64),
        ),
        migrations.AlterField(
            model_name='hook',
            name='module',
            field=models.CharField(help_text='The name of the module, within the hook_modules filder, that will be run when this hook triggers', max_length=32),
        ),
        migrations.AlterField(
            model_name='hook',
            name='path',
            field=models.CharField(help_text='The last parameter of the url this hook will have. FOr example, co.aiesec.org/podio/hooks/*path*', max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='hook',
            name='uses',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='N\xfamero de veces que ha sido usado este hook'),
        ),
    ]