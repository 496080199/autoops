# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0014_auto_20151109_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('con_name', models.CharField(max_length=50, verbose_name=b'\xe9\x85\x8d\xe7\xbd\xae\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'db_table': 'configure',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('f_name', models.CharField(max_length=50, verbose_name=b'\xe6\x96\x87\xe4\xbb\xb6\xe5\x90\x8d')),
                ('f_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\x97\xb6\xe9\x97\xb4')),
                ('f_file', models.FileField(upload_to=b'./conf/', verbose_name=b'\xe6\x96\x87\xe4\xbb\xb6')),
                ('f_configure', models.ForeignKey(to='info.Configure')),
            ],
            options={
                'db_table': 'file',
            },
        ),
        migrations.CreateModel(
            name='Handler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('h_name', models.CharField(max_length=50, verbose_name=b'\xe5\xa4\x84\xe7\x90\x86\xe5\x9d\x97\xe5\x90\x8d')),
                ('h_service', models.CharField(max_length=50, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x90\x8d')),
                ('h_staus', models.CharField(max_length=50, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe7\x8a\xb6\xe6\x80\x81')),
                ('h_configure', models.ForeignKey(to='info.Configure')),
            ],
            options={
                'db_table': 'handler',
            },
        ),
        migrations.CreateModel(
            name='Mod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('m_name', models.CharField(max_length=50, verbose_name=b'\xe6\xa8\xa1\xe5\x9d\x97\xe5\x90\x8d\xe7\xa7\xb0')),
                ('m_value', models.CharField(max_length=50, verbose_name=b'\xe6\xa8\xa1\xe5\x9d\x97\xe5\x8f\x82\xe6\x95\xb0')),
            ],
            options={
                'db_table': 'mod',
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('p_name', models.CharField(max_length=50, verbose_name=b'\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe7\xa7\xb0')),
                ('p_value', models.CharField(max_length=50, verbose_name=b'\xe5\x8f\x82\xe6\x95\xb0\xe5\x80\xbc')),
                ('p_configure', models.ForeignKey(to='info.Configure')),
            ],
            options={
                'db_table': 'parameter',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('t_name', models.CharField(max_length=50, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x90\x8d\xe7\xa7\xb0')),
                ('t_configure', models.ForeignKey(to='info.Configure')),
            ],
            options={
                'db_table': 'task',
            },
        ),
        migrations.CreateModel(
            name='Yum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('yum_name', models.CharField(max_length=50, verbose_name=b'yum\xe5\x90\x8d\xe7\xa7\xb0')),
                ('yum_state', models.CharField(max_length=50, verbose_name=b'yum\xe7\x8a\xb6\xe6\x80\x81')),
                ('yum_configure', models.ForeignKey(to='info.Mod')),
            ],
            options={
                'db_table': 'yum',
            },
        ),
        migrations.AddField(
            model_name='mod',
            name='m_configure',
            field=models.ForeignKey(to='info.Task'),
        ),
    ]
