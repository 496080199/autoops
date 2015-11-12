# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0016_auto_20151109_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='f_configure',
        ),
        migrations.RemoveField(
            model_name='handler',
            name='h_configure',
        ),
        migrations.RemoveField(
            model_name='mod',
            name='m_task',
        ),
        migrations.RemoveField(
            model_name='parameter',
            name='p_configure',
        ),
        migrations.RemoveField(
            model_name='task',
            name='t_configure',
        ),
        migrations.RemoveField(
            model_name='yum',
            name='yum_mod',
        ),
        migrations.AddField(
            model_name='configure',
            name='con_path',
            field=models.CharField(default=datetime.datetime(2015, 11, 10, 9, 32, 10, 341000, tzinfo=utc), max_length=100, verbose_name=b'\xe6\x96\x87\xe4\xbb\xb6\xe8\xb7\xaf\xe5\xbe\x84'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configure',
            name='con_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 10, 9, 32, 31, 388000, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.DeleteModel(
            name='Handler',
        ),
        migrations.DeleteModel(
            name='Mod',
        ),
        migrations.DeleteModel(
            name='Parameter',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.DeleteModel(
            name='Yum',
        ),
    ]
