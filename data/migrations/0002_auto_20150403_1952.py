# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_squashed_0004_auto_20150222_2002'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['display_order'], 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='coach',
            name='player',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='data.Player'),
        ),
    ]
