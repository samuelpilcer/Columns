# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_auto_20171029_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='ranking',
            field=models.FloatField(default=0),
        ),
    ]
