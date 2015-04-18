# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Your name')),
                ('message', models.CharField(max_length=255, verbose_name=b'Message')),
                ('photo', models.ImageField(upload_to=b'slideshow', verbose_name=b'Photo')),
            ],
        ),
    ]
