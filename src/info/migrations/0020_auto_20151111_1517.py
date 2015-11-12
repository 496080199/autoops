# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0019_auto_20151111_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configure',
            name='con_name',
            field=models.CharField(max_length=200, verbose_name=b'\xe9\x85\x8d\xe7\xbd\xae\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
    ]
