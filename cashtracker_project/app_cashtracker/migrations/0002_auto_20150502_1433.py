# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_cashtracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True
                    )
                ),
                ('value', models.FloatField(default=0.0)),
                ('currency', models.CharField(default='BGN', max_length=3)),
                ('category', models.IntegerField()),
                ('subcategory', models.IntegerField()),
                (
                    'date_time',
                    models.DateTimeField(
                        verbose_name='date and time created'
                    )
                ),
                ('name', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=1000)),
                ('user_id', models.IntegerField()),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='salary',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=255),
        ),
    ]
