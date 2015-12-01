# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.db.models.fields.related import OneToOneField
from django.forms.models import ModelForm, ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from ckeditor.fields import RichTextFormField
import os,re
#from django.http.response import HttpResponse
#from ljcms.settings import MEDIA_ROOT
#from ckeditor import widgets


# Create your models here.
class Group(models.Model):
    g_name=models.CharField("服务器组名",max_length=50,unique=True)
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
    s_monitor=models.BooleanField("是否开启监控",default=False)
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
    g_server=ModelMultipleChoiceField(queryset=Server.objects.all(),required=False)
    def __init__(self, *args, **kwargs):
        super(GroupForm,self).__init__( *args, **kwargs)
        if 'instance' in kwargs:
            self.fields['g_server'].initial=self.instance.server_set.all()
        
    def save(self, *args, **kwargs):
        super(GroupForm,self).save(*args, **kwargs)
        self.instance.server_set.clear()
        for server in self.cleaned_data['g_server']:
            self.instance.server_set.add(server)
            
    def clean_g_name(self):
        name=self.cleaned_data['g_name']
        for i in name:
            if i >=u'u4e00' and i <= u'\u9fa5':
                raise forms.ValidationError("必须全输入为英文")
            
        return name
    class Meta:
        model=Group
        exclude='',
        
class ServerConfigure(models.Model):
    ser_name=models.CharField("配置名称",max_length=200,unique=True)
    ser_time=models.DateTimeField(auto_now=True)
    ser_path=models.CharField("配置路径",max_length=100)
    ser_status=models.CharField("配置状态",max_length=255,null=True)
    ser_server=models.ForeignKey(Server)
    def __unicode__(self):
        return self.ser_name
    class Meta:
        db_table="server_configure"
        
class ServerConfigureForm(ModelForm):
    class Meta:
        model=ServerConfigure
        fields=['ser_name']
class ServerConfigureEditForm(ModelForm):
    ser_filecontent=RichTextFormField()
    class Meta:
        model=ServerConfigure
        fields=['ser_filecontent']
class ServerConfigureActionForm(ModelForm):
    class Meta:
        model=ServerConfigure
        fields=['ser_name']
        
class ServerConfigureTime(models.Model):
    conf=OneToOneField(ServerConfigure)
    ser_minute=models.CharField("分",default='*',max_length=100)
    ser_hour=models.CharField("时",default='*',max_length=100)
    ser_day=models.CharField("天",default='*',max_length=100)
    ser_month=models.CharField("月",default='*',max_length=100)
    ser_weekday=models.CharField("周",default='*',max_length=100)
    ser_jobpath=models.CharField("任务路径",max_length=100)
    ser_jobstatus=models.BooleanField("是否开启",default=False)
    ser_leapyear=models.BooleanField("是否闰年",default=False)
    class Meta:
        db_table="server_configure_time"
class ServerConfigureTimeForm(ModelForm):
    def clean_ser_minute(self):
        minute=self.cleaned_data['ser_minute']
        if minute=='*':
            return minute
        if re.match(r'\*\/', minute):
            re_minute=minute.split('/')
            if len(re_minute)==2:
                if re_minute[1].isdigit():
                    return minute
        if re.findall(r'\,',minute):
            list1=minute.split(',')
            list2=set(list1)
            if len(list1)==len(list2):
                for i in list1:
                    if i.isdigit() and int(i) in range(0,59):
                        continue
                    raise forms.ValidationError("请输入一个有效值（参考crontab）")
                return minute      
        if minute.isdigit():
            if int(minute)>=0 and int(minute)<=59:
                return minute
        raise forms.ValidationError("请输入一个有效值（参考crontab）")
        return minute
    def clean_ser_hour(self):
        hour=self.cleaned_data['ser_hour']
        if hour=='*':
            return hour
        if re.match(r'\*\/', hour):
            re_hour=hour.split('/')
            if len(re_hour)==2:
                if re_hour[1].isdigit():
                    return hour
        if re.findall(r'\,',hour):
            list1=hour.split(',')
            list2=set(list1)
            if len(list1)==len(list2):
                for i in list1:
                    if i.isdigit() and int(i) in range(0,23):
                        continue
                    raise forms.ValidationError("请输入一个有效值（参考crontab）")
                return hour
        if hour.isdigit():
            if int(hour)>=0 and int(hour)<=23:
                return hour
        raise forms.ValidationError("请输入一个有效值（参考crontab）")
        return hour
    def clean_ser_day(self):
        day=self.cleaned_data['ser_day']
        month=self['ser_month'].value()
        leapyear=self['ser_leapyear'].value()
        if day=='*':
            return day
        if month=='*':
            if day.isdigit():
                if int(day)>=1 and int(day)<=31:
                    return day
        if re.match(r'\*\/', day):
            re_day=day.split('/')
            if len(re_day)==2:
                if re_day[1].isdigit():
                    return day
        if re.findall(r'\,',day):
            list1=day.split(',')
            list2=set(list1)
            if len(list1)==len(list2):
                for i in list1:
                    if i.isdigit() and int(i) in range(1,31):
                        continue
                    raise forms.ValidationError("请输入一个有效值（参考crontab）")
                return day
        if month.isdigit():
            if int(month) in [1,3,5,7,8,10,12]:
                if day.isdigit():
                    if int(day)>=1 and int(day)<=31:
                        return day
            elif int(month) in [4,6,9,12]:
                if day.isdigit():
                    if int(day)>=1 and int(day)<=30:
                        return day
            elif int(month)==2:
                if day.isdigit():
                    if leapyear==0:
                        if int(day)>=1 and int(day)<=28:
                            return day
                    else:
                        if int(day)>=1 and int(day)<=29:
                            return day      
        raise  forms.ValidationError("请输入一个有效值（参考crontab）")   
        return day
    def clean_ser_month(self):
        month=self.cleaned_data['ser_month']
        if month=='*':
            return month
        if re.match(r'\*\/', month):
            re_month=month.split('/')
            if len(re_month)==2:
                if re_month[1].isdigit():
                    return month
        if re.findall(r'\,',month):
            list1=month.split(',')
            list2=set(list1)
            if len(list1)==len(list2):
                for i in list1:
                    if i.isdigit() and int(i) in range(1,12):
                        continue
                    raise forms.ValidationError("请输入一个有效值（参考crontab）")
                return month
        if month.isdigit():
            if int(month)>=1 and int(month)<=12:
                return month
        raise forms.ValidationError("请输入一个有效值（参考crontab）")
        return month
    def clean_ser_weekday(self):
        weekday=self.cleaned_data['ser_weekday']
        if weekday=='*':
            return weekday
        if re.match(r'\*\/', weekday):
            re_weekday=weekday.split('/')
            if len(re_weekday)==2:
                if re_weekday[1].isdigit():
                    return weekday
        if re.findall(r'\,',weekday):
            list1=weekday.split(',')
            list2=set(list1)
            if len(list1)==len(list2):
                for i in list1:
                    if i.isdigit() and int(i) in range(1,12):
                        continue
                    raise forms.ValidationError("请输入一个有效值（参考crontab）")
                return weekday
        if weekday.isdigit():
            if int(weekday)>=1 and int(weekday)<=7:
                return weekday
        raise forms.ValidationError("请输入一个有效值（1-7或*）")
        return weekday       
    class Meta:
        model=ServerConfigureTime
        fields=['ser_minute','ser_hour','ser_day','ser_month','ser_weekday','ser_jobstatus','ser_leapyear']
        
                                
        
class GroupConfigure(models.Model):
    gro_name=models.CharField("配置名称",max_length=200)
    gro_time=models.DateTimeField(auto_now=True)
    gro_path=models.CharField("配置路径",max_length=100)
    gro_status=models.CharField("配置状态",max_length=255,null=True)
    gro_group=models.ForeignKey(Group)
    def __unicode__(self):
        return self.gro_name
    class Meta:
        db_table="group_configure"
class GroupConfigureForm(ModelForm):
    class Meta:
        model=GroupConfigure
        fields=['gro_name']
class GroupConfigureEditForm(ModelForm):
    gro_filecontent=RichTextFormField()
    class Meta:
        model=GroupConfigure
        fields=['gro_filecontent']
class GroupConfigureActionForm(ModelForm):
    class Meta:
        model=GroupConfigure
        fields=['gro_name']
        
class GroupConfigureTime(models.Model):
    conf=OneToOneField(GroupConfigure)
    gro_minute=models.CharField("分",default='*',max_length=100)
    gro_hour=models.CharField("时",default='*',max_length=100)
    gro_day=models.CharField("天",default='*',max_length=100)
    gro_month=models.CharField("月",default='*',max_length=100)
    gro_weekday=models.CharField("周",default='*',max_length=100)
    gro_jobpath=models.CharField("任务路径",max_length=100)
    gro_jobstatus=models.BooleanField("是否开启",default=False)
    gro_leapyear=models.BooleanField("是否闰年",default=False)
    class Meta:
        db_table="group_configure_time"
class GroupConfigureTimeForm(ModelForm):
    def clean_gro_minute(self):
        minute=self.cleaned_data['gro_minute']
        if minute=='*':
            return minute
        if re.match(r'\*\/', minute):
            re_minute=minute.split('/')
            if len(re_minute)==2:
                if re_minute[1].isdigit():
                    return minute
        if re.findall(r'\,',minute):
            list1=minute.split(',')
            list2=set(list1)
            if len(list1)==len(list2):
                for i in list1:
                    if i.isdigit() and int(i) in range(0,59):
                        continue
                    raise forms.ValidationError("请输入一个有效值（参考crontab）")
                return minute      
        if minute.isdigit():
            if int(minute)>=0 and int(minute)<=59:
                return minute
        raise forms.ValidationError("请输入一个有效值（参考crontab）")
        return minute
    def clean_gro_hour(self):
        hour=self.cleaned_data['gro_hour']
        if hour=='*':
            return hour
        if re.match(r'\*\/', hour):
            re_hour=hour.split('/')
            if len(re_hour)==2:
                if re_hour[1].isdigit():
                    return hour
        if re.findall(r'\,',hour):
            list1=hour.split(',')
            list2=set(list1)
            if len(list1)==len(list2):
                for i in list1:
                    if i.isdigit() and int(i) in range(0,23):
                        continue
                    raise forms.ValidationError("请输入一个有效值（参考crontab）")
                return hour
        if hour.isdigit():
            if int(hour)>=0 and int(hour)<=23:
                return hour
        raise forms.ValidationError("请输入一个有效值（参考crontab）")
        return hour
    def clean_gro_day(self):
        day=self.cleaned_data['gro_day']
        month=self['gro_month'].value()
        leapyear=self['gro_leapyear'].value()
        if day=='*':
            return day
        if month=='*':
            if day.isdigit():
                if int(day)>=1 and int(day)<=31:
                    return day
        if re.match(r'\*\/', day):
            re_day=day.split('/')
            if len(re_day)==2:
                if re_day[1].isdigit():
                    return day
        if re.findall(r'\,',day):
            list1=day.split(',')
            list2=set(list1)
            if len(list1)==len(list2):
                for i in list1:
                    if i.isdigit() and int(i) in range(1,31):
                        continue
                    raise forms.ValidationError("请输入一个有效值（参考crontab）")
                return day
        if month.isdigit():
            if int(month) in [1,3,5,7,8,10,12]:
                if day.isdigit():
                    if int(day)>=1 and int(day)<=31:
                        return day
            elif int(month) in [4,6,9,12]:
                if day.isdigit():
                    if int(day)>=1 and int(day)<=30:
                        return day
            elif int(month)==2:
                if day.isdigit():
                    if leapyear==0:
                        if int(day)>=1 and int(day)<=28:
                            return day
                    else:
                        if int(day)>=1 and int(day)<=29:
                            return day      
        raise  forms.ValidationError("请输入一个有效值（参考crontab）")   
        return day
    def clean_gro_month(self):
        month=self.cleaned_data['gro_month']
        if month=='*':
            return month
        if re.match(r'\*\/', month):
            re_month=month.split('/')
            if len(re_month)==2:
                if re_month[1].isdigit():
                    return month
        if re.findall(r'\,',month):
            list1=month.split(',')
            list2=set(list1)
            if len(list1)==len(list2):
                for i in list1:
                    if i.isdigit() and int(i) in range(1,12):
                        continue
                    raise forms.ValidationError("请输入一个有效值（参考crontab）")
                return month
        if month.isdigit():
            if int(month)>=1 and int(month)<=12:
                return month
        raise forms.ValidationError("请输入一个有效值（参考crontab）")
        return month
    def clean_gro_weekday(self):
        weekday=self.cleaned_data['gro_weekday']
        if weekday=='*':
            return weekday
        if re.match(r'\*\/', weekday):
            re_weekday=weekday.split('/')
            if len(re_weekday)==2:
                if re_weekday[1].isdigit():
                    return weekday
        if re.findall(r'\,',weekday):
            list1=weekday.split(',')
            list2=set(list1)
            if len(list1)==len(list2):
                for i in list1:
                    if i.isdigit() and int(i) in range(1,12):
                        continue
                    raise forms.ValidationError("请输入一个有效值（参考crontab）")
                return weekday
        if weekday.isdigit():
            if int(weekday)>=1 and int(weekday)<=7:
                return weekday
        raise forms.ValidationError("请输入一个有效值（1-7或*）")
        return weekday       
    class Meta:
        model=GroupConfigureTime
        fields=['gro_minute','gro_hour','gro_day','gro_month','gro_weekday','gro_jobstatus','gro_leapyear']
        
                                
        
class File(models.Model):
    f_path=models.CharField("文件路径",max_length=100)
    def __unicode__(self):
        return self.id
    class Meta:
        db_table="file"
class FileForm(ModelForm):
    f_file=forms.FileField()
    #def clean_f_file(self):
    #    f_file=self.cleaned_data['f_file']
    #    content=f_file.readline()
     #   char=chardet.detect(content)
    #    if char['encoding']=='ascii':
    #        return f_file
    #    raise forms.ValidationError("请上传utf8编码的文本类文件")
    #    return f_file
            
    class Meta:
        model=File
        fields=['f_file']
class FileEditForm(ModelForm):
    f_filecontent=RichTextFormField()
    class Meta:
        model=File
        fields=['f_filecontent']
    
class Log(models.Model):
    time=models.DateTimeField(auto_now=True)
    server=models.ForeignKey(Server)
    class Meta:
        db_table="log"
class Load(models.Model):
    ldavg1=models.CharField(max_length=200)
    ldavg5=models.CharField(max_length=200)
    ldavg10=models.CharField(max_length=200)
    log=models.ForeignKey(Log)
    class Meta:
        db_table="load"
class Cpu(models.Model):
    dev=models.CharField(max_length=200)
    user=models.CharField(max_length=200)
    nice=models.CharField(max_length=200)
    system=models.CharField(max_length=200)
    iowait=models.CharField(max_length=200)
    steal=models.CharField(max_length=200)
    idle=models.CharField(max_length=200)
    log=models.ForeignKey(Log)
    class Meta:
        db_table="cpu"
class Mem(models.Model):
    kbmemfree=models.CharField(max_length=200)
    kbmemused=models.CharField(max_length=200)
    memused=models.CharField(max_length=200)
    log=models.ForeignKey(Log)
    class Meta:
        db_table="mem"
class Disk(models.Model):
    mount=models.CharField(max_length=200)
    used=models.CharField(max_length=200)
    avail=models.CharField(max_length=200)
    use=models.CharField(max_length=200)
    log=models.ForeignKey(Log)
    class Meta:
        db_table="disk"
class Io(models.Model): 
    dev=models.CharField(max_length=200)
    tps=models.CharField(max_length=200)
    rd_sec=models.CharField(max_length=200)  
    wd_sec=models.CharField(max_length=200)
    util=models.CharField(max_length=200) 
    log=models.ForeignKey(Log)
    class Meta:
        db_table="io"  
class Network(models.Model):
    dev=models.CharField(max_length=200)
    rxpck=models.CharField(max_length=200)
    txpck=models.CharField(max_length=200)
    rxbyt=models.CharField(max_length=200)
    txbyt=models.CharField(max_length=200)
    log=models.ForeignKey(Log) 
    class Meta:
        db_table="network"
        
        
class Tip(models.Model):
    method=models.CharField(max_length=200,unique=True)
    content=models.CharField(max_length=1000)
    class Meta:
        db_table="tip"
    
        
        

