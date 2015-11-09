# -*- coding: utf-8 -*-
from django.db import models
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
    con_name=models.CharField("配置名称",max_length=50)
    class Meta:
        db_table="configure"
class File(models.Model):
    f_name=models.CharField("文件名",max_length=50)
    f_time=models.DateTimeField("上传时间",auto_now=True)
    f_file=models.FileField("文件",upload_to='./conf/')
    f_configure=models.ForeignKey(Configure)
    class Meta:
        db_table="file"
class Parameter(models.Model):
    p_name=models.CharField("参数名称",max_length=50)
    p_value=models.CharField("参数值",max_length=50)
    p_configure=models.ForeignKey(Configure)
    class Meta:
        db_table="parameter"
class Handler(models.Model):
    h_name=models.CharField("处理块名",max_length=50)
    h_service=models.CharField("服务名",max_length=50)
    h_staus=models.CharField("服务状态",max_length=50)
    h_configure=models.ForeignKey(Configure)
    class Meta:
        db_table="handler"
class Task(models.Model):
    t_name=models.CharField("任务名称",max_length=50)
    t_configure=models.ForeignKey(Configure)
    class Meta:
        db_table="task"
class Mod(models.Model):
    m_name=models.CharField("模块名称",max_length=50)
    m_task=models.ForeignKey(Task)
    class Meta:
        db_table="mod"
class Yum(models.Model):
    yum_name=models.CharField("yum名称",max_length=50)
    yum_state=models.CharField("yum状态",max_length=50)
    yum_mod=models.ForeignKey(Mod)
    class Meta:
        db_table="yum"
    
    
    
    
    
    
    
    
    
    
    
    
    
