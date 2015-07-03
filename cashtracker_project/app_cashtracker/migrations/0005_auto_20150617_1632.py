# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_cashtracker', '0004_user_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='report',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='reporthascategories',
            name='category_id',
        ),
        migrations.RemoveField(
            model_name='reporthascategories',
            name='report_id',
        ),
        migrations.RemoveField(
            model_name='reporthaspayments',
            name='payment_id',
        ),
        migrations.RemoveField(
            model_name='reporthaspayments',
            name='report_id',
        ),
        migrations.RemoveField(
            model_name='reporthassubcategories',
            name='report_id',
        ),
        migrations.RemoveField(
            model_name='reporthassubcategories',
            name='subcategory_id',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='category_id',
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(default=1, to='app_cashtracker.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(default=1, to='app_cashtracker.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(default=1, to='app_cashtracker.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reporthascategories',
            name='category',
            field=models.ForeignKey(default=1, to='app_cashtracker.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reporthascategories',
            name='report',
            field=models.ForeignKey(default=1, to='app_cashtracker.Report'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reporthaspayments',
            name='payment',
            field=models.ForeignKey(default=1, to='app_cashtracker.Payment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reporthaspayments',
            name='report',
            field=models.ForeignKey(default=1, to='app_cashtracker.Report'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reporthassubcategories',
            name='report',
            field=models.ForeignKey(default=1, to='app_cashtracker.Report'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reporthassubcategories',
            name='subcategory',
            field=models.ForeignKey(
                default=1,
                to='app_cashtracker.Subcategory'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(default=1, to='app_cashtracker.Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='category',
            field=models.ForeignKey(to='app_cashtracker.Category'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='comment',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='payment',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='payment',
            name='subcategory',
            field=models.ForeignKey(to='app_cashtracker.Subcategory'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='value',
            field=models.DecimalField(
                max_digits=19,
                default=0.0,
                decimal_places=3
            ),
        ),
        migrations.AlterField(
            model_name='report',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='salary',
            field=models.DecimalField(
                max_digits=19,
                default=0.0,
                decimal_places=3
            ),
        ),
    ]
