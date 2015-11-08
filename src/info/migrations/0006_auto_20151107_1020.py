# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0005_auto_20151107_0959'),
    ]

    operations = [
        migrations.RenameField(
            model_name='software',
            old_name='so_id',
            new_name='so_server',
        ),
        migrations.RemoveField(
            model_name='software',
            name='so_ip',
        ),
    ]
