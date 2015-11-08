# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0009_auto_20151108_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='s_status',
            field=models.CharField(max_length=30, null=True, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe8\xbf\x9e\xe6\x8e\xa5\xe7\x8a\xb6\xe6\x80\x81'),
        ),
    ]
