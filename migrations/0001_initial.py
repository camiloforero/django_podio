# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aplicacion',
            fields=[
                ('nombre', models.CharField(unique=True, max_length=32)),
                ('app_id', models.CharField(max_length=8, serialize=False, primary_key=True)),
                ('app_token', models.CharField(help_text='Escribe ac\xe1 el token de la aplicaci\xf3n. \xc9ste lo puedes encontrar en PODIO dentro de la parte de desarrolladores. Alternativamente, escribe tu token personal si quieres que las acciones que hace esta aplicaci\xf3n se hagan en tu nombre', max_length=32)),
                ('link', models.URLField()),
            ],
            options={
                'verbose_name_plural': 'aplicaciones',
            },
        ),
        migrations.CreateModel(
            name='Campo',
            fields=[
                ('nombre', models.CharField(max_length=32)),
                ('id', models.CharField(max_length=16, serialize=False, primary_key=True)),
                ('external_id', models.CharField(max_length=32)),
            ],
        ),
    ]
