# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0010_auto_20151108_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardware',
            name='h_diskmodel',
            field=models.CharField(max_length=100, verbose_name=b'\xe7\xa1\xac\xe7\x9b\x98\xe5\x9e\x8b\xe5\x8f\xb7'),
        ),
        migrations.AlterField(
            model_name='hardware',
            name='h_disktotal',
            field=models.CharField(max_length=100, verbose_name=b'\xe7\xa1\xac\xe7\x9b\x98\xe5\xa4\xa7\xe5\xb0\x8f'),
        ),
    ]
