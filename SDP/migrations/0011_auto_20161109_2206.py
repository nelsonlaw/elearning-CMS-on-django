# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-09 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SDP', '0010_auto_20161109_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='progress',
            field=models.IntegerField(default=1),
        ),
    ]
