# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_podio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aplicacion',
            name='nombre2',
            field=models.CharField(default='asd', unique=True, max_length=32),
            preserve_default=False,
        ),
    ]
