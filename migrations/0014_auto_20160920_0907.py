# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_podio', '0013_auto_20160910_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hook',
            name='name',
            field=models.CharField(help_text='The last parameter of the url this hook will have. FOr example, co.aiesec.org/podio/hooks/*name*', max_length=32, primary_key=True, serialize=False),
        ),
    ]