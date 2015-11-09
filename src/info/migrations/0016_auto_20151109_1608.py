# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0015_auto_20151109_1606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mod',
            old_name='m_configure',
            new_name='m_task',
        ),
        migrations.RenameField(
            model_name='yum',
            old_name='yum_configure',
            new_name='yum_mod',
        ),
    ]
