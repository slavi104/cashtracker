# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_cashtracker', '0005_auto_20150617_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='url',
            field=models.CharField(default='', max_length=255),
        ),
    ]
