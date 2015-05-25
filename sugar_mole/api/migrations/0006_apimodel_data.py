# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20150517_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='apimodel',
            name='data',
            field=models.TextField(default=datetime.datetime(2015, 5, 25, 12, 38, 48, 883710, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
