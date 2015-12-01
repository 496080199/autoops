# coding: utf-8 
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from info.models import *
from info.models import ServerForm,GroupForm
from django.http.response import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from ljcms.settings import MEDIA_ROOT, MEDIA_URL
#from ansible.playbook import PlayBook
#from ansible import callbacks
#from ansible import utils
import os,chardet,time,random,stat,paramiko,commands,shutil
import datetime


# Create your views here.
#def index(request):
#       return render(request,'software.html')

def server(request):
    servers=Server.objects.all()
    
    page_size=10
    paginator=Paginator(servers,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        server_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        server_list=paginator.page(paginator.num_pages)
        
    tip=get_tip('server')
    #serverfields=Server._meta.get_all_field_names()

    context={'server_list':server_list,'tip':tip}
    #return HttpResponse(serverfields)
#    return render(request,'server.html',context)
    return render_to_response('server.html', context, context_instance=RequestContext(request))

def server_add(request):
    if request.method=='POST':
        form=ServerForm(request.POST)
        if form.is_valid():
            form.save()
            
            server_now=Server.objects.get(s_ip=form['s_ip'].value())
            hardware=Hardware(h_server=server_now,h_type='-',h_cpu='-',h_core=0,h_diskmodel='-',h_disktotal='-',h_mem='-')
            software=Software(so_server=server_now,so_servername='-',so_serverrel='-',so_kernel='-',so_python='-')
            hardware.save()
            software.save()
            copy_sshkey(form['s_ip'].value())
            server_infoupdate(form['s_ip'].value())
            return HttpResponseRedirect('/')        
    else:
        form=ServerForm()
        tip=get_tip('server_add')
    return render_to_response('server_add.html',{'form':form,'tip':tip})
def server_edit(request,ip):
    server_now=Server.objects.get(s_ip=ip)
    if request.method=='POST':
        form=ServerForm(request.POST,instance=server_now)
        if form.is_valid():
            form.save()
            copy_sshkey(form['s_ip'].value())
            server_infoupdate(form['s_ip'].value())
            return HttpResponseRedirect('/') 
    else:
        form=ServerForm(instance=server_now)
        tip=get_tip('server_edit')

    return render(request,'server_edit.html',{'form':form,'tip':tip})
def server_infoupdate(ip):
    server_now=Server.objects.get(s_ip=ip)
    fp=open("/tmp/host",'w')
    fp.write(server_now.s_ip)
    fp.close()
    import ansible.runner
    runner=ansible.runner.Runner(
                                 host_list='/tmp/host',
                                 pattern=str(ip),
                                 remote_user=server_now.s_user,
                                 remote_pass=server_now.s_password,
                                 remote_port=server_now.s_port,
                                 module_name='setup',
                                 module_args='',
    )
    data=runner.run()
    if data['contacted']!={}:
        ob=data['contacted'][server_now.s_ip]['ansible_facts']
        server_now.hardware.h_type=ob['ansible_product_name']
        if ob['ansible_machine']=='x86_64' or ob['ansible_machine']=='x86':
            server_now.hardware.h_cpu=ob['ansible_processor'][1]
        else:
            server_now.hardware.h_cpu=ob['ansible_processor'][0]
        server_now.hardware.h_core=ob['ansible_processor_cores']
        server_now.hardware.h_diskmodel=''
        server_now.hardware.h_disktotal=''
        for mount in ob['ansible_mounts']:
            server_now.hardware.h_diskmodel+=str(mount['mount'])+'\r\n'
            size_total=float(mount['size_total'])/1024/1024/1024
            server_now.hardware.h_disktotal+=str(float('%0.3f'%size_total))+'GB\r\n'
        server_now.hardware.h_mem=str(ob['ansible_memtotal_mb'])+'MB'
        server_now.software.so_servername=ob['ansible_distribution']
        server_now.software.so_serverrel=ob['ansible_distribution_version']
        server_now.software.so_kernel=ob['ansible_kernel']
        server_now.software.so_python=ob['ansible_python_version']
        server_now.s_status="OK"
    else:
        server_now.s_status=data['dark'][server_now.s_ip]['msg']
            
    server_now.hardware.save()
    server_now.software.save()
    server_now.save()
    return
def server_del(request,ip):
    server_now=Server.objects.get(s_ip=ip)
    serconfs=server_now.serverconfigure_set.all()
    for serconf in serconfs:
        del_server_clear(serconf.id)
    server_now.delete()
    return HttpResponseRedirect('/') 
def copy_sshkey(ip):
    server=Server.objects.get(s_ip=ip)
    sshkey_path=os.path.expanduser('~/.ssh/id_rsa.pub')
    if not os.path.exists(sshkey_path):
        HttpResponse("请到服务器上生成公钥，路径为：~/.ssh/id_rsa.pub")
    ssh_key=open(sshkey_path,'r').read()
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server.s_ip, username=server.s_user, password=server.s_password,port=server.s_port,timeout=10)
        client.exec_command('mkdir -p ~/.ssh/')
        client.exec_command('echo "%s" >> ~/.ssh/authorized_keys' % ssh_key)
        client.exec_command('chmod 644 ~/.ssh/authorized_keys')
        client.exec_command('chmod 700 ~/.ssh/')
    except Exception,e:
        print e
    client.close()
    return ssh_key
 
    
def group(request):
    groups=Group.objects.all()
    
    page_size=10
    paginator=Paginator(groups,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        group_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        group_list=paginator.page(paginator.num_pages)
    tip=get_tip('group')
    return render(request,'group.html',{'group_list':group_list,'tip':tip})
def group_add(request):
    if request.method=='POST':
        form=GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/group/') 
    else:
        form=GroupForm()
    tip=get_tip('group_add')
    return render_to_response('group_add.html',{'form':form,'tip':tip}) 
def group_edit(request,id):
    group_now=Group.objects.get(id=id)
    if request.method=='POST':
        form=GroupForm(request.POST,instance=group_now)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/group/')
    else:
        form=GroupForm(instance=group_now)
    tip=get_tip('group_edit')
    return render_to_response('group_edit.html',{'form':form,'id':id,'tip':tip})
def group_del(request,id):
    group_now=Group.objects.get(id=id)
    for gro_conf in group_now.groupconfigure_set.all():
        del_group_clear(gro_conf.id)
        gro_conf.delete()
    group_now.delete()
    return HttpResponseRedirect('/group/')  

def server_inv_update():
    servers=Server.objects.all()
    ips=[]
    for server in servers:
        ips.append(str(server.s_ip))
    result='{"all":{"hosts":'+str(ips)+'}}'
    path=MEDIA_ROOT+'/server_inv.py'
    f=open(path,'w')
    content='#!/usr/bin/env python\nimport json\n\nprint json.dumps('+result+')\n'
    f.write(content)
    f.close()
    os.chmod(path,stat.S_IRWXU)
    return
        

def group_inv_update():
    groups=Group.objects.all()
    result='{'
    for group in groups:
        ips=[]
        for server in group.server_set.all():
            ips.append(str(server.s_ip))
        group_str='"'+ str(group.g_name)+'":{"hosts":'+str(ips)+'},'
        result+=group_str
    result+='}' 
    path=MEDIA_ROOT+'/group_inv.py'
    f=open(path,'w')
    content='#!/usr/bin/env python\nimport json\n\nprint json.dumps('+result+')\n'
    f.write(content)
    f.close()
    os.chmod(path,stat.S_IRWXU)
    return content
   
def hardware(request):
    hardwares=Hardware.objects.all()
    
    page_size=10
    paginator=Paginator(hardwares,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        hardware_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        hardware_list=paginator.page(paginator.num_pages)
    tip=get_tip('hardware')
    context={'hardware_list':hardware_list,'tip':tip}
    return render_to_response('hardware.html', context, context_instance=RequestContext(request))
#    return render(request,'hardware.html')
def software(request):
    softwares=Software.objects.all()
    
    page_size=10
    paginator=Paginator(softwares,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        software_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        software_list=paginator.page(paginator.num_pages)
    tip=get_tip('software')
    context={'software_list':software_list,'tip':tip}
    return render_to_response('software.html', context, context_instance=RequestContext(request))

def server_configure(request):
    servers=Server.objects.all()
    page_size=10
    paginator=Paginator(servers,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        server_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        server_list=paginator.page(paginator.num_pages)
    tip=get_tip('server_configure')
    context={'server_list':server_list,'tip':tip}
    return render_to_response('server_configure.html',context, context_instance=RequestContext(request))

def server_configure_manage(request,id):
    server=Server.objects.get(id=id)
    server_configures=server.serverconfigure_set.all()
    page_size=10
    paginator=Paginator(server_configures,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        server_configure_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        server_configure_list=paginator.page(paginator.num_pages)
    down_path=MEDIA_URL
    upload_path=MEDIA_ROOT+'/'
    tip=get_tip('server_configure_manage')
    context={'server_configure_list':server_configure_list,'server':server,'down_path':down_path,'upload_path':upload_path,'tip':tip}
    return render_to_response('server_configure_manage.html',context, context_instance=RequestContext(request))

def server_configure_new(request,id):
    server=Server.objects.get(id=id)
    if request.method=="POST":
        form=ServerConfigureForm(request.POST)   
        if form.is_valid():
            serconf=ServerConfigure()
            #serconf_time.serverconfigure.add(serconf)
            file_name=form['ser_name'].value()
            path=MEDIA_ROOT+"/yml/server/"
            if not os.path.exists(path):
                os.makedirs(path)
            file_path=path+file_name+time.strftime('_%Y%m%d%H%M%S')+'.yml'
            dst=open(file_path,'wt')
            line=r'---'+'\n'+'- hosts: '+server.s_ip+'\n  port: '+str(server.s_port)+'\n  #hosts和port信息自动生成，请勿修改或重复添加\n'
            dst.write(line)
            dst.close()
            serconf.ser_name=file_name
            serconf.ser_path=file_path
            server.serverconfigure_set.add(serconf)
            serconf.save()
            serconf_time=ServerConfigureTime(conf=serconf)
            serconf_time.save()
            server_configure_change(serconf.id)
            return HttpResponseRedirect('/server_configure_manage/'+str(server.id)) 
            
    else:
        form=ServerConfigureForm()
    tip=get_tip('server_configure_manage_new')
    return render_to_response('server_configure_new.html',{'form':form,'server':server,'tip':tip}) 

def server_configure_edit(request,id):
    serconf=ServerConfigure.objects.get(id=id)
    server_id=str(serconf.ser_server.id)
    if request.method=='POST':
        form=ServerConfigureEditForm(request.POST)
        if form.is_valid():
            try:
                sercon_file=open(serconf.ser_path,'w')
                sercon_file.write(form['ser_filecontent'].value().encode("utf8"))
                sercon_file.close()
                serconf.save()
                server_configure_change(serconf.id)
                return HttpResponseRedirect('/server_configure_manage/'+server_id)
            except IOError as e:
                print e
                
    else:
        serconf_file=open(serconf.ser_path,'rt')
        content=serconf_file.read().decode("utf8")
        form=ServerConfigureEditForm({'ser_filecontent':content})
        serconf_file.close()
    tip=get_tip('server_configure_manage_edit')
    return render_to_response('server_configure_edit.html',{'form':form,'serconf_ser_name':serconf.ser_name,'id':id,'server_id':server_id,'tip':tip})

def server_configure_del(request,id):
    serconf=ServerConfigure.objects.get(id=id)
    server_id=str(serconf.ser_server.id)
    del_server_clear(id)
    serconf.delete()
    return HttpResponseRedirect('/server_configure_manage/'+server_id)
def del_server_clear(id):
    serconf=ServerConfigure.objects.get(id=id)
    try:
        os.remove(serconf.ser_path)
        os.remove(serconf.serverconfiguretime.ser_jobpath)
        shutil.rmtree(MEDIA_ROOT+'/yml/time/server/'+serconf.ser_name)
    except Exception,e:
        print e
    command='ansible "127.0.0.1" -m cron -a "name="server_'+serconf.ser_name+'" state=absent"'
    r=commands.getstatusoutput(command)
    return r
    

def server_configure_action(request,id):
    server_inv_update()
    serconf=ServerConfigure.objects.get(id=id)
    server_id=str(serconf.ser_server.id)
    if request.method=='POST':
        form=ServerConfigureEditForm(request.POST)
        path=MEDIA_ROOT+'/server_inv.py'
        r=commands.getstatusoutput('ansible-playbook -i '+path+' '+serconf.ser_path)
        #fp=open("/tmp/server",'w')
        #fp.write(serconf.ser_server.s_ip)
        #fp.close()
        #utils.VERBOSITY = 0
        #playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        #stats = callbacks.AggregateStats()
        #runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
        #pb=PlayBook(playbook=serconf.ser_path,host_list=path,remote_port=serconf.ser_server.s_port,timeout=30,callbacks=playbook_cb,runner_callbacks=runner_cb,stats=stats)
        #results=pb.run()
        #r=results[str(serconf.ser_server.s_ip)]
        action_result=r[1]
        #if r['ok'] > 0:
        #    action_result="执行成功"
        tip=get_tip('server_configure_result')
        content={'action_result':action_result,'server_id':server_id,'tip':tip}
        
        return render_to_response('server_configure_result.html',content)
    else:
        form=ServerConfigureActionForm({'ser_name':serconf.ser_name})
    tip=get_tip('server_configure_action')
    return render_to_response('server_configure_action.html',{'form':form,'id':id,'server_ip':serconf.ser_server.s_ip,'server_id':server_id,'tip':tip})
def server_configure_time(request,id):
    server_inv_update()
    serconf=ServerConfigure.objects.get(id=id)
    serconf_time=serconf.serverconfiguretime
    server_id=str(serconf.ser_server.id)
    if request.method=='POST':
        form=ServerConfigureTimeForm(request.POST,instance=serconf_time)
        if form.is_valid():
            ser_shell=serconf_time.ser_jobpath
            minute=form['ser_minute'].value()
            hour=form['ser_hour'].value()
            day=form['ser_day'].value()
            month=form['ser_month'].value()
            weekday=form['ser_weekday'].value()
            serconf_time.ser_jobstatus=form['ser_jobstatus'].value()
            if form['ser_jobstatus'].value()!=0: 
                if ser_shell=='':
                    inv_path=MEDIA_ROOT+'/server_inv.py'
                    path=MEDIA_ROOT+'/yml/time/server/'
                    log_path=MEDIA_ROOT+'/yml/time/server/'+serconf.ser_name+'/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    if not os.path.exists(log_path):
                        os.makedirs(log_path)
                    ser_shell=path+serconf.ser_name+time.strftime('_%Y%m%d%H%M%S')+'.sh'
                    f=open(ser_shell,'w')
                    content='#!/bin/sh\nansible-playbook -i '+inv_path+' '+serconf.ser_path+' > '+log_path+'`date +%Y%m%d%H%M%S`'+'.log'
                    f.write(content)
                    f.close()
                    os.chmod(ser_shell,stat.S_IRWXU)
                command='ansible "127.0.0.1" -m cron -a "name="server_'+serconf.ser_name+'" minute="'+minute+'" hour="'+hour+'" day="'+day+'" month="'+month+'" weekday="'+weekday+'" job="'+ser_shell+'""'
                commands.getstatusoutput(command)
            else:
                command='ansible "127.0.0.1" -m cron -a "name="server_'+serconf.ser_name+'" state=absent"'
                commands.getstatusoutput(command)
            serconf_time.ser_jobpath=ser_shell
            serconf_time.ser_minute=minute
            serconf_time.ser_hour=hour
            serconf_time.ser_day=day
            serconf_time.ser_month=month
            serconf_time.ser_weekday=weekday
            serconf_time.save()
            return HttpResponseRedirect('/server_configure_manage/'+server_id)
    else:
        year=int(time.strftime('%Y'))
        serconf_time.ser_leapyear=False
        if (year%4==0 and year%100!=0) or year%400==0:
            serconf_time.ser_leapyear=True
        serconf_time.save()
        form=ServerConfigureTimeForm(instance=serconf.serverconfiguretime)
    tip=get_tip('server_configure_time')
    return render_to_response('server_configure_time.html',{'form':form,'serconf_name':serconf.ser_name,'id':id,'server_id':server_id,'tip':tip})
    
def server_configure_time_log(request,id):  
    serconf=ServerConfigure.objects.get(id=id)
    server_id=str(serconf.ser_server.id)
    log_path=MEDIA_ROOT+'/yml/time/server/'+serconf.ser_name+'/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)  
    logs=os.listdir(log_path)
    page_size=10
    paginator=Paginator(logs,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        log_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        log_list=paginator.page(paginator.num_pages)
    tip=get_tip('server_configure_time_log')
    return render_to_response('server_configure_time_log.html',{'log_list':log_list,'serconf_name':serconf.ser_name,'id':id,'server_id':server_id,'tip':tip})
def server_configure_time_log_open(request,id,log): 
    serconf=ServerConfigure.objects.get(id=id)
    log_path=MEDIA_ROOT+'/yml/time/server/'+serconf.ser_name+'/'
    logfile=log_path+log
    try:
        f=open(logfile,'r')
        result=f.read()
    except Exception,e:
        print e
    f.close()
    tip=get_tip('server_configure_time_logresult')
    return render_to_response('server_configure_time_logresult.html',{'result':result,'log':log,'id':id,'tip':tip})
def server_configure_time_log_del(request,id,log):
    serconf=ServerConfigure.objects.get(id=id)
    log_path=MEDIA_ROOT+'/yml/time/server/'+serconf.ser_name+'/'
    logfile=log_path+log
    try:
        os.remove(logfile)
    except Exception,e:
        print e   
    return HttpResponseRedirect('/server_configure_time_log/'+id)
def server_configure_time_log_delall(request,id): 
    serconf=ServerConfigure.objects.get(id=id)
    log_path=MEDIA_ROOT+'/yml/time/server/'+serconf.ser_name+'/'
    logs=os.listdir(log_path)
    for log in logs:
        try:
            os.remove(log_path+log)
        except Exception,e:
            print e   
    return HttpResponseRedirect('/server_configure_time_log/'+id)

def server_configure_change(id):
    serconf=ServerConfigure.objects.get(id=id)
    result=commands.getstatusoutput('ansible-playbook --syntax-check '+serconf.ser_path)
    if result[0]!=0:
        serconf.ser_status=result[1]
        serconf.save()
        return serconf.id
    serconf.ser_status='OK'
    serconf.save()
    return serconf.id

def group_configure(request):
    groups=Group.objects.all()
    page_size=10
    paginator=Paginator(groups,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        group_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        group_list=paginator.page(paginator.num_pages)
    tip=get_tip('group_configure')
    context={'group_list':group_list,'tip':tip}
    return render_to_response('group_configure.html',context, context_instance=RequestContext(request))

def group_configure_manage(request,id):
    group=Group.objects.get(id=id)
    group_configures=group.groupconfigure_set.all()
    page_size=10
    paginator=Paginator(group_configures,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        group_configure_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        group_configure_list=paginator.page(paginator.num_pages)
    down_path=MEDIA_URL
    upload_path=MEDIA_ROOT+'/'
    tip=get_tip('group_configure_manage')
    context={'group_configure_list':group_configure_list,'group':group,'down_path':down_path,'upload_path':upload_path,'tip':tip}
    return render_to_response('group_configure_manage.html',context, context_instance=RequestContext(request))

def group_configure_new(request,id):
    group=Group.objects.get(id=id)
    if request.method=="POST":
        form=GroupConfigureForm(request.POST)   
        if form.is_valid():
            groconf=GroupConfigure()
            file_name=form['gro_name'].value()
            path=MEDIA_ROOT+"/yml/group/"
            if not os.path.exists(path):
                os.makedirs(path)
            file_path=path+file_name+time.strftime('_%Y%m%d%H%M%S')+'.yml'
            dst=open(file_path,'wt')
            line='---\n- hosts: '+group.g_name+'\n  #hosts automatic generated,not change\n'
            dst.write(line)
            dst.close()
            groconf.gro_name=file_name
            groconf.gro_path=file_path
            group.groupconfigure_set.add(groconf)
            groconf.save()
            groconf_time=GroupConfigureTime(conf=groconf)
            groconf_time.save()
            group_configure_change(groconf.id)
            return HttpResponseRedirect('/group_configure_manage/'+str(group.id)) 
            
    else:
        form=GroupConfigureForm()
    tip=get_tip('group_configure_new')
    return render_to_response('group_configure_new.html',{'form':form,'group':group,'tip':tip}) 

def group_configure_edit(request,id):
    groconf=GroupConfigure.objects.get(id=id)
    group_id=str(groconf.gro_group.id)
    if request.method=='POST':
        form=GroupConfigureEditForm(request.POST)
        if form.is_valid():
            try:
                grocon_file=open(groconf.gro_path,'w')
                grocon_file.write(form['gro_filecontent'].value().encode("utf8"))
                grocon_file.close()
                groconf.save()
                group_configure_change(groconf.id)
                return HttpResponseRedirect('/group_configure_manage/'+group_id)
            except IOError as e:
                print e
                
    else:
        groconf_file=open(groconf.gro_path,'rt')
        content=groconf_file.read().decode("utf8")
        form=GroupConfigureEditForm({'gro_filecontent':content})
        groconf_file.close()
    tip=get_tip('group_configure_edit')
    return render_to_response('group_configure_edit.html',{'form':form,'groconf_gro_name':groconf.gro_name,'id':id,'group_id':group_id,'tip':tip})

def group_configure_del(request,id):
    groconf=GroupConfigure.objects.get(id=id)
    group_id=str(groconf.gro_group.id)
    del_group_clear(id)
    groconf.delete()
    return HttpResponseRedirect('/group_configure_manage/'+group_id)
def del_group_clear(id):
    groconf=GroupConfigure.objects.get(id=id)
    try:
        os.remove(groconf.gro_path)
        os.remove(groconf.groupconfiguretime.gro_jobpath)
        shutil.rmtree(MEDIA_ROOT+'/yml/time/group/'+groconf.gro_name)
    except Exception,e:
        print e
    command='ansible "127.0.0.1" -m cron -a "name="group_'+groconf.gro_name+'" state=absent"'
    r=commands.getstatusoutput(command)
    return r

def group_configure_action(request,id):
    group_inv_update()
    groconf=GroupConfigure.objects.get(id=id)
    group_id=str(groconf.gro_group.id)
    if request.method=='POST':
        form=GroupConfigureEditForm(request.POST)
        path=MEDIA_ROOT+'/group_inv.py'
        r=commands.getstatusoutput('ansible-playbook -i '+path+' '+groconf.gro_path)
        action_result=r[1]
        #if r['ok'] > 0:
        #    action_result="执行成功"
        #utils.VERBOSITY = 0
        #playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        #stats = callbacks.AggregateStats()
        #runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
        #pb=PlayBook(playbook=groconf.gro_path,host_list=path,timeout=30,callbacks=playbook_cb,runner_callbacks=runner_cb,stats=stats)
        #results=pb.run()
        #servers=groconf.gro_group.server_set.all()
        #action_results=[]
        #for server in servers:
        #    if results[str(server.s_ip)]['ok'] > 0:
        #        action_results.append(str(server.s_ip)+"执行成功")
        #    else:
        #        action_results.append(str(server.s_ip)+"执行失败，请检查您的playbook文件")
        
        #r=results[str(serconf.ser_server.s_ip)]
        #action_result="执行失败,请检查您的playbook文件"
        #if r['ok'] > 0:
        #    action_result="执行成功"
        content={'action_result':action_result,'gro_gname':groconf.gro_group.g_name,'group_id':group_id}
        return render_to_response('group_configure_result.html',content)
    else:
        form=GroupConfigureActionForm({'gro_name':groconf.gro_name})
    tip=get_tip('group_configure_action')
    return render_to_response('group_configure_action.html',{'form':form,'id':id,'g_name':groconf.gro_group.g_name,'group_id':group_id,'tip':tip})

def group_configure_time(request,id):
    group_inv_update()
    groconf=GroupConfigure.objects.get(id=id)
    groconf_time=groconf.groupconfiguretime
    group_id=str(groconf.gro_group.id)
    if request.method=='POST':
        form=GroupConfigureTimeForm(request.POST,instance=groconf_time)
        if form.is_valid():
            gro_shell=groconf_time.gro_jobpath
            minute=form['gro_minute'].value()
            hour=form['gro_hour'].value()
            day=form['gro_day'].value()
            month=form['gro_month'].value()
            weekday=form['gro_weekday'].value()
            groconf_time.gro_jobstatus=form['gro_jobstatus'].value()
            if form['gro_jobstatus'].value()!=0: 
                if gro_shell=='':
                    inv_path=MEDIA_ROOT+'/group_inv.py'
                    path=MEDIA_ROOT+'/yml/time/group/'
                    log_path=MEDIA_ROOT+'/yml/time/group/'+groconf.gro_name+'/'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    if not os.path.exists(log_path):
                        os.makedirs(log_path)
                    gro_shell=path+groconf.gro_name+time.strftime('_%Y%m%d%H%M%S')+'.sh'
                    f=open(gro_shell,'w')
                    content='#!/bin/sh\nansible-playbook -i '+inv_path+' '+groconf.gro_path+' > '+log_path+'`date +%Y%m%d%H%M%S`'+'.log'
                    f.write(content)
                    f.close()
                    os.chmod(gro_shell,stat.S_IRWXU)
                command='ansible "127.0.0.1" -m cron -a "name="group_'+groconf.gro_name+'" minute="'+minute+'" hour="'+hour+'" day="'+day+'" month="'+month+'" weekday="'+weekday+'" job="'+gro_shell+'""'
                commands.getstatusoutput(command)
            else:
                command='ansible "127.0.0.1" -m cron -a "name="group_'+groconf.gro_name+'" state=absent"'
                commands.getstatusoutput(command)
            groconf_time.gro_jobpath=gro_shell
            groconf_time.gro_minute=minute
            groconf_time.gro_hour=hour
            groconf_time.gro_day=day
            groconf_time.gro_month=month
            groconf_time.gro_weekday=weekday
            groconf_time.save()
            return HttpResponseRedirect('/group_configure_manage/'+group_id)
    else:
        year=int(time.strftime('%Y'))
        groconf_time.gro_leapyear=False
        if (year%4==0 and year%100!=0) or year%400==0:
            groconf_time.gro_leapyear=True
        groconf_time.save()
        form=GroupConfigureTimeForm(instance=groconf.groupconfiguretime)
    tip=get_tip('group_configure_time')
    return render_to_response('group_configure_time.html',{'form':form,'groconf_name':groconf.gro_name,'id':id,'group_id':group_id,'tip':tip})
    
def group_configure_time_log(request,id):  
    groconf=GroupConfigure.objects.get(id=id)
    group_id=str(groconf.gro_group.id)
    log_path=MEDIA_ROOT+'/yml/time/group/'+groconf.gro_name+'/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)  
    logs=os.listdir(log_path)
    page_size=10
    paginator=Paginator(logs,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        log_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        log_list=paginator.page(paginator.num_pages)
    tip=get_tip('group_configure_time_log')
    return render_to_response('group_configure_time_log.html',{'log_list':log_list,'groconf_name':groconf.gro_name,'id':id,'group_id':group_id,'tip':tip})
def group_configure_time_log_open(request,id,log): 
    groconf=GroupConfigure.objects.get(id=id)
    log_path=MEDIA_ROOT+'/yml/time/group/'+groconf.gro_name+'/'
    logfile=log_path+log
    try:
        f=open(logfile,'r')
        result=f.read()
    except Exception,e:
        print e
    f.close()
    tip=get_tip('group_configure_time_logresult')
    return render_to_response('group_configure_time_logresult.html',{'result':result,'log':log,'id':id,'tip':tip})
def group_configure_time_log_del(request,id,log):
    groconf=GroupConfigure.objects.get(id=id)
    log_path=MEDIA_ROOT+'/yml/time/group/'+groconf.gro_name+'/'
    logfile=log_path+log
    try:
        os.remove(logfile)
    except Exception,e:
        print e   
    return HttpResponseRedirect('/group_configure_time_log/'+id)
def group_configure_time_log_delall(request,id): 
    groconf=GroupConfigure.objects.get(id=id)
    log_path=MEDIA_ROOT+'/yml/time/group/'+groconf.gro_name+'/'
    logs=os.listdir(log_path)
    for log in logs:
        try:
            os.remove(log_path+log)
        except Exception,e:
            print e   
    return HttpResponseRedirect('/group_configure_time_log/'+id)

def group_configure_change(id):
    groconf=GroupConfigure.objects.get(id=id)
    result=commands.getstatusoutput('ansible-playbook --syntax-check '+groconf.gro_path)
    if result[0]!=0:
        groconf.gro_status=result[1]
        groconf.save()
        return groconf.id
    groconf.gro_status='OK'
    groconf.save()
    return groconf.id
def filelist(request):
    files=File.objects.all()
    page_size=10
    paginator=Paginator(files,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        file_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        file_list=paginator.page(paginator.num_pages)
    tip=get_tip('filelist')
    context={'file_list':file_list,'tip':tip}
    return render_to_response('filelist.html',context, context_instance=RequestContext(request))
def file_upload(request):
    if request.method=='POST':
        form=FileForm(request.POST,request.FILES) 
        if form.is_valid():
            f=File()
            f.f_path=handle_upload(request.FILES['f_file'])
            f.save()
            return HttpResponseRedirect('/filelist/') 
    else:
        form=FileForm()
    tip=get_tip('file_upload')
    return render_to_response('file_upload.html',{'form':form,'tip':tip}) 
def handle_upload(f):
    try:
        path=MEDIA_ROOT+"/yml/file/"
        if not os.path.exists(path):
            os.makedirs(path)
        f_name=''.join(f.name.split('.')[0:-1])
        f_prefix=f.name.split('.')[-1]
        f_random=str(int(random.uniform(0.1,1)*1000000))
        f_path=path+f_name+f_random+'.'+f_prefix
        dst=open(f_path,'wb+')
        for chunk in f.chunks():
            dst.write(chunk)
        dst.close()
    except Exception,e:
        print e
    return f_path
def file_edit(request,id):
    f=File.objects.get(id=id)
    if request.method=='POST':
        form=FileEditForm(request.POST)
        if form.is_valid():
            try:
                f_file=open(f.f_path,'w')
                f_file.write(form['f_filecontent'].value().encode("utf8"))
                f_file.close()
                f.save()
                return HttpResponseRedirect('/filelist/')
            except IOError as e:
                print e
                
    else:
        path=MEDIA_ROOT+'/yml/file/'
        f_path=f.f_path
        f_file=open(f.f_path,'rt')
        #return HttpResponse(f.f_path.encode('utf8'))
        content=f_file.read()
        char=chardet.detect(content)
        if char['encoding']!='ascii':
            return render_to_response('file_unedit.html')
        form=FileEditForm({'f_filecontent':content})
        f_file.close()
        tip=get_tip('file_edit')
    return render_to_response('file_edit.html',{'form':form,'id':id,'path':path,'f_path':f_path,'tip':tip})
def file_del(request,id):
    f=File.objects.get(id=id)
    try:
        os.remove(f.f_path)
    except Exception,e:
        print e
    f.delete()
    return HttpResponseRedirect('/filelist/') 

def server_monitor(request):
    servers=Server.objects.all()
    page_size=10
    paginator=Paginator(servers,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        server_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        server_list=paginator.page(paginator.num_pages)
    tip=get_tip('server_monitor')
    context={'server_list':server_list,'tip':tip}
#    return render(request,'server.html',context)
    return render_to_response('server_monitor.html', context, context_instance=RequestContext(request))
    
def server_monitor_view(request,id,t):
    server=Server.objects.get(id=id)
    now=datetime.datetime.now()
    time={
        '1': now+datetime.timedelta(hours=-1),
        '6': now+datetime.timedelta(hours=-6),
        '24': now+datetime.timedelta(hours=-24)
    }              
    log_set=server.log_set.filter(time__range=(time[str(t)],now))
    x=[]
    ldavg1=[]
    ldavg5=[]
    ldavg10=[]
    user=[]
    nice=[]
    system=[]
    iowait=[]
    steal=[]
    idle=[]
    kbmemfree=[]
    kbmemused=[]
    mount={}
    num={}
    iodev={}
    num1={}
    netdev={}
    num2={}
    for log in log_set:
        x.append(str(log.time))
        loads=log.load_set.all()
        for load in loads:
            ldavg1.append(load.ldavg1)
            ldavg5.append(load.ldavg5)
            ldavg10.append(load.ldavg10)
        cpus=log.cpu_set.all()
        for cpu in cpus:
            user.append(cpu.user)
            nice.append(cpu.nice)
            system.append(cpu.system)
            iowait.append(cpu.iowait)
            steal.append(cpu.steal)
            idle.append(cpu.idle)
        mems=log.mem_set.all()
        for mem in mems:
            kbmemfree.append(mem.kbmemfree)
            kbmemused.append(mem.kbmemused)
        disks=log.disk_set.all()
        n=1
        for disk in disks:
            mount.setdefault(n,{'未用':[],'已用':[]})
            num.setdefault(n,disk.mount)
            
            mount[n]['已用'].append(disk.used)
            mount[n]['未用'].append(disk.avail)
            #mount[n]['use'].append(disk.use)
            n+=1
        ios=log.io_set.all()
        n1=1
        for io in ios:
            iodev.setdefault(n1,{'利用率':[]})
            num1.setdefault(n1,io.dev)
            iodev[n1]['利用率'].append(io.util)
            n1+=1
        networks=log.network_set.all()
        n2=1
        for network in networks:
            netdev.setdefault(n2,{'接收':[],'发送':[]})
            num2.setdefault(n2,network.dev)
            netdev[n2]['接收'].append(network.rxbyt)
            netdev[n2]['发送'].append(network.txbyt)
            n2+=1
        
    tip=get_tip('server_monitor_view')
    content={'x':x,'ldavg1':ldavg1,'ldavg5':ldavg5,'ldavg10':ldavg10,'user':user,'nice':nice,'system':system,'iowait':iowait,'steal':steal,'idle':idle,'kbmemfree':kbmemfree,'kbmemused':kbmemused,'mount':mount,"num":num,'iodev':iodev,'num1':num1,'netdev':netdev,'num2':num2,'server_ip':server.s_ip,'id':id,'t':t,'tip':tip}
    #return HttpResponse(num.items())
    
    return render_to_response('server_monitor_view.html',content, context_instance=RequestContext(request))

def group_monitor(request):
    groups=Group.objects.all()
    page_size=10
    paginator=Paginator(groups,page_size)
    try:
        page=int(request.GET.get('page','1'))
    except ValueError:
        page=1
    try:
        group_list=paginator.page(page)
    except (EmptyPage,InvalidPage):
        group_list=paginator.page(paginator.num_pages)
    tip=get_tip('group_monitor')
    context={'group_list':group_list,'tip':tip}
#    return render(request,'server.html',context)
    return render_to_response('group_monitor.html', context, context_instance=RequestContext(request))

def group_monitor_view(request,id,t,type):
    group=Group.objects.get(id=id)
    servers=group.server_set.all()
    now=datetime.datetime.now()
    time={
        '1': now+datetime.timedelta(hours=-1),
        '6': now+datetime.timedelta(hours=-6),
        '24': now+datetime.timedelta(hours=-24)
    }
    x=[]
    result={}
    num={}
    numm={}
    n=1
    
    for server in servers:
        x=[]
        log_set=server.log_set.filter(time__range=(time[str(t)],now))
        ip=server.s_ip
        num.setdefault(n,ip)
        if type=='load':
            result.setdefault(n,{type:{'一分钟平均负载':[],'五分钟平均负载':[],'十分钟平均负载':[]}}) 
            for log in log_set:
                x.append(str(log.time))
                for load in log.load_set.all():
                    result[n][type]['一分钟平均负载'].append(load.ldavg1)
                    result[n][type]['五分钟平均负载'].append(load.ldavg5)
                    result[n][type]['十分钟平均负载'].append(load.ldavg10)
        if type=='cpu':
            result.setdefault(n,{type:{'用户':[],'优先级':[],'系统':[],'读写等待':[],'虚拟':[],'空闲':[]}}) 
            for log in log_set:
                x.append(str(log.time))
                for cpu in log.cpu_set.all():
                    result[n][type]['用户'].append(cpu.user)
                    result[n][type]['优先级'].append(cpu.nice)
                    result[n][type]['系统'].append(cpu.system)
                    result[n][type]['读写等待'].append(cpu.iowait)
                    result[n][type]['虚拟'].append(cpu.steal)
                    result[n][type]['空闲'].append(cpu.idle)
        if type=='mem':
            result.setdefault(n,{type:{'未用':[],'已用':[]}}) 
            for log in log_set:
                x.append(str(log.time))
                for mem in log.mem_set.all():
                    result[n][type]['未用'].append(mem.kbmemfree)
                    result[n][type]['已用'].append(mem.kbmemused)
        if type=='disk':
            numm.setdefault(n,{})
            result.setdefault(n,{type:{}}) 
            for log in log_set:
                x.append(str(log.time))
                m=1
                for disk in log.disk_set.all(): 
                    result[n][type].setdefault(m,{'未用':[],'已用':[]})
                    numm[n].setdefault(m,disk.mount)
                    result[n][type][m]['未用'].append(disk.avail)
                    result[n][type][m]['已用'].append(disk.used)
                    m+=1          
        if type=='io':
            numm.setdefault(n,{})
            result.setdefault(n,{type:{}}) 
            for log in log_set:
                x.append(str(log.time))
                m=1
                for io in log.io_set.all(): 
                    result[n][type].setdefault(m,{'利用率':[]})
                    numm[n].setdefault(m,io.dev)
                    result[n][type][m]['利用率'].append(io.util)
                    m+=1 
        if type=='network':
            numm.setdefault(n,{})
            result.setdefault(n,{type:{}}) 
            for log in log_set:
                x.append(str(log.time))
                m=1
                for network in log.network_set.all(): 
                    result[n][type].setdefault(m,{'接收':[],'发送':[]})
                    numm[n].setdefault(m,network.dev)
                    result[n][type][m]['接收'].append(network.rxbyt)
                    result[n][type][m]['发送'].append(network.txbyt)
                    m+=1             
        n+=1
        
    #return HttpResponse(x)
    tip=get_tip('group_monitor_view')
    content={'x':x,'result':result,'num':num,'type':type,'numm':numm,'group_name':group.g_name,'id':id,'t':t,'tip':tip}
    return render_to_response('group_monitor_view.html',content, context_instance=RequestContext(request))

def get_tip(method):
    try:
        tip=Tip.objects.get(method=method)
    except Exception:
        tip=Tip.objects.get(method='default')

    return tip.content.split(';')