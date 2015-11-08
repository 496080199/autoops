# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_auto_20151106_1555'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hardware',
            old_name='h_id',
            new_name='h_server',
        ),
        migrations.RemoveField(
            model_name='hardware',
            name='h_ip',
        ),
    ]
