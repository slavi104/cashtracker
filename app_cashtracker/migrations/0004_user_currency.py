# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_cashtracker', '0003_category_report_reporthascategories_reporthaspayments_reporthassubcategories_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='currency',
            field=models.CharField(default='BGN', max_length=255),
        ),
    ]
