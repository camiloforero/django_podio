# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_podio', '0002_aplicacion_nombre2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aplicacion',
            name='nombre2',
        ),
    ]
