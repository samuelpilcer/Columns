# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-10-18 10:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='contenu',
            field=models.TextField(null=True),
        ),
    ]
