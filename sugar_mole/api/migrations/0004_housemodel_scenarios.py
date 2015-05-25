# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_apimodel_housemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='housemodel',
            name='scenarios',
            field=models.ManyToManyField(to='api.ScenarioModel'),
            preserve_default=True,
        ),
    ]
