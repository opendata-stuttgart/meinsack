# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_area_pickupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='district_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
