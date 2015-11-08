# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0011_auto_20151108_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardware',
            name='h_cpu',
            field=models.CharField(max_length=50, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8cpu'),
        ),
    ]
