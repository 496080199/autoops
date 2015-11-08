# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_remove_server_s_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='g_server',
        ),
        migrations.AddField(
            model_name='server',
            name='s_group',
            field=models.ManyToManyField(to='info.Group'),
        ),
    ]
