# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('g_name', models.CharField(max_length=50, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\xbb\x84\xe5\x90\x8d')),
                ('g_desc', models.CharField(max_length=50, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\xbb\x84\xe7\xbb\x84\xe6\x8f\x8f\xe8\xbf\xb0')),
            ],
            options={
                'db_table': 'group',
            },
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('h_type', models.CharField(max_length=100, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe4\xba\xa7\xe5\x93\x81\xe5\x9e\x8b\xe5\x8f\xb7')),
                ('h_cpu', models.CharField(max_length=50, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8cpu')),
                ('h_core', models.IntegerField()),
                ('h_diskmodel', models.CharField(max_length=100, verbose_name=b'\xe7\xa1\xac\xe7\x9b\x98\xe5\x9e\x8b\xe5\x8f\xb7')),
                ('h_disktotal', models.CharField(max_length=100, verbose_name=b'\xe7\xa1\xac\xe7\x9b\x98\xe5\xa4\xa7\xe5\xb0\x8f')),
                ('h_mem', models.CharField(max_length=10, verbose_name=b'\xe5\x86\x85\xe5\xad\x98\xe5\xa4\xa7\xe5\xb0\x8f')),
            ],
            options={
                'db_table': 'hardware',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('s_ip', models.GenericIPAddressField(unique=True, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8IP')),
                ('s_name', models.CharField(max_length=50, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe5\x90\x8d\xe7\xa7\xb0')),
                ('s_user', models.CharField(max_length=20, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d')),
                ('s_password', models.CharField(max_length=50, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe5\xaf\x86\xe7\xa0\x81')),
                ('s_port', models.IntegerField(verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8SSH\xe7\xab\xaf\xe5\x8f\xa3')),
                ('s_status', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe8\xbf\x9e\xe6\x8e\xa5\xe7\x8a\xb6\xe6\x80\x81')),
                ('s_group', models.ManyToManyField(to='info.Group')),
            ],
            options={
                'db_table': 'server',
            },
        ),
        migrations.CreateModel(
            name='ServerConfigure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('con_name', models.CharField(max_length=200, verbose_name=b'\xe9\x85\x8d\xe7\xbd\xae\xe5\x90\x8d\xe7\xa7\xb0')),
                ('con_time', models.DateTimeField(auto_now=True)),
                ('con_path', models.CharField(max_length=100, verbose_name=b'\xe9\x85\x8d\xe7\xbd\xae\xe8\xb7\xaf\xe5\xbe\x84')),
                ('con_status', models.CharField(max_length=255, null=True, verbose_name=b'\xe9\x85\x8d\xe7\xbd\xae\xe7\x8a\xb6\xe6\x80\x81')),
                ('con_server', models.ForeignKey(to='info.Server')),
            ],
            options={
                'db_table': 'configure',
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('so_servername', models.CharField(max_length=20, verbose_name=b'\xe7\xb3\xbb\xe7\xbb\x9f\xe5\x90\x8d')),
                ('so_serverrel', models.CharField(max_length=10, verbose_name=b'\xe7\xb3\xbb\xe7\xbb\x9f\xe7\x89\x88\xe6\x9c\xac')),
                ('so_kernel', models.CharField(max_length=30, verbose_name=b'\xe5\x86\x85\xe6\xa0\xb8')),
                ('so_python', models.CharField(max_length=10, verbose_name=b'python\xe7\x89\x88\xe6\x9c\xac')),
                ('so_server', models.OneToOneField(to='info.Server')),
            ],
            options={
                'db_table': 'software',
            },
        ),
        migrations.AddField(
            model_name='hardware',
            name='h_server',
            field=models.OneToOneField(to='info.Server'),
        ),
    ]
