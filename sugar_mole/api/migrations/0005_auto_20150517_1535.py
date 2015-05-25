# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0004_housemodel_scenarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtraData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('push_data', models.TextField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='housemodel',
            name='api_available',
            field=models.ManyToManyField(to='api.APIModel', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='housemodel',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='housemodel',
            name='scenarios',
            field=models.ManyToManyField(to='api.ScenarioModel', blank=True),
            preserve_default=True,
        ),
    ]
