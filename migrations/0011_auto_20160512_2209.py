# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_podio', '0010_auto_20160512_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='hook',
            name='label',
            field=models.CharField(default='empty', max_length=64, verbose_name='A human readable name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hook',
            name='field',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='If empty, this will be an app hook. If not, it will be an app_field hook. One main difference is that with an item.update trigger, the frist one will be triggered every time anything is modified, while the second will trigger only when the specific field is modificed'),
        ),
        migrations.AlterField(
            model_name='hook',
            name='module',
            field=models.CharField(max_length=32, verbose_name='The name of the module, within the hook_modules filder, that will be run when this hook triggers'),
        ),
        migrations.AlterField(
            model_name='hook',
            name='path',
            field=models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='The last parameter of the url this hook will have. FOr example, co.aiesec.org/podio/hooks/*path*'),
        ),
    ]