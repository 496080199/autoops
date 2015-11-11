# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.db.models.fields.related import OneToOneField
from django.forms.models import ModelForm, ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

# Create your models here.
class Group(models.Model):
    g_name=models.CharField("服务器组名",max_length=50)
    g_desc=models.CharField("服务器组组描述",max_length=50)
    def __unicode__(self):
        return self.g_name
    class Meta:
        db_table="group"
class Server(models.Model):
    s_ip=models.GenericIPAddressField("服务器IP",unique=True)
    s_name=models.CharField("服务器名称",max_length=50)
    s_group=models.ManyToManyField(Group)
    s_user=models.CharField("服务器用户名",max_length=20)
    s_password=models.CharField("服务器密码",max_length=50)
    s_port=models.IntegerField("服务器SSH端口")
    s_status=models.CharField("服务器连接状态",max_length=255,null=True)
    def __unicode__(self):
        return self.s_name
    class Meta:
        db_table="server"
class Hardware(models.Model):
    h_server=OneToOneField(Server)
    h_type=models.CharField("服务器产品型号",max_length=100)
    h_cpu=models.CharField("服务器cpu",max_length=50)
    h_core=models.IntegerField()
    h_diskmodel=models.CharField("硬盘型号",max_length=100)
    h_disktotal=models.CharField("硬盘大小",max_length=100)
    h_mem=models.CharField("内存大小",max_length=10)
    def __unicode__(self):
        return self.s_type
    class Meta:
        db_table="hardware"
class Software(models.Model):
    so_server=OneToOneField(Server)
    so_servername=models.CharField("系统名",max_length=20)
    so_serverrel=models.CharField("系统版本",max_length=10)
    so_kernel=models.CharField("内核",max_length=30)
    so_python=models.CharField("python版本",max_length=10)
   
    class Meta:
        db_table="software"
        
        
class ServerForm(ModelForm):
#    s_group=ModelMultipleChoiceField(
#        queryset=Group.objects.order_by('id'),
#        required=True,
#        label="服务器组",
#        error_messages={'required':'至少选择一个'},
#        widget=CheckboxSelectMultiple,
#        )
    class Meta:
        model=Server
        exclude='s_status',
class GroupForm(ModelForm):
    class Meta:
        model=Group
        exclude='',
        
class Configure(models.Model):
    con_name=models.CharField("配置名称",max_length=200)
    con_time=models.DateTimeField(auto_now=True)
    con_path=models.CharField("文件路径",max_length=100)
    class Meta:
        db_table="configure"
class ConfigureForm(ModelForm):
    con_file=forms.FileField()
    def clean_con_file(self):
        name_suffix=self.cleaned_data["con_file"].name.split('.')[1]
        if name_suffix != 'yaml':
            raise forms.ValidationError("请上传一个yaml格式文件")
        return self.cleaned_data["con_file"]
    class Meta:
        model=Configure
        exclude='con_name','con_time','con_path',

    
    
    
    
    
