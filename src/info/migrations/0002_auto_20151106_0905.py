# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='s_group',
            field=models.CharField(max_length=255, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\xbb\x84'),
        ),
        migrations.AlterField(
            model_name='server',
            name='s_ip',
            field=models.GenericIPAddressField(unique=True, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8IP'),
        ),
    ]
