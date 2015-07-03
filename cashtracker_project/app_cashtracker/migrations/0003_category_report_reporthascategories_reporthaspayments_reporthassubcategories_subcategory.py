# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_cashtracker', '0002_auto_20150502_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        auto_created=True,
                        serialize=False,
                        primary_key=True
                    )
                ),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('user_id', models.IntegerField()),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        auto_created=True,
                        serialize=False,
                        primary_key=True
                    )
                ),
                ('user_id', models.IntegerField()),
                ('created', models.DateTimeField(verbose_name='date created')),
                ('report_type', models.CharField(max_length=255)),
                (
                    'report_date',
                    models.DateTimeField(
                        verbose_name='report date used for report_type'
                    )
                ),
                (
                    'start_date',
                    models.DateTimeField(
                        verbose_name='start date'
                    )
                ),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('currency', models.CharField(max_length=3, default='BGN')),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ReportHasCategories',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        auto_created=True,
                        serialize=False,
                        primary_key=True
                    )
                ),
                ('report_id', models.IntegerField()),
                ('category_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ReportHasPayments',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        auto_created=True,
                        serialize=False,
                        primary_key=True
                    )
                ),
                ('report_id', models.IntegerField()),
                ('payment_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ReportHasSubcategories',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        auto_created=True,
                        serialize=False,
                        primary_key=True
                    )
                ),
                ('report_id', models.IntegerField()),
                ('subcategory_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        auto_created=True,
                        serialize=False,
                        primary_key=True
                    )
                ),
                ('name', models.CharField(max_length=255)),
                ('category_id', models.IntegerField()),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
    ]
