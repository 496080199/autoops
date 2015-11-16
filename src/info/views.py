# coding: utf-8 
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from info.models import *
from info.models import ServerForm,GroupForm
from django.http.response import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from ljcms.settings import MEDIA_ROOT, MEDIA_URL
import os,time

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

    context={'server_list':server_list}
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
    return render_to_response('server_add.html',{'form':form,})
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
    return render(request,'server_edit.html',{'form':form})
def server_infoupdate(ip):
    server_now=Server.objects.get(s_ip=ip)
    fp=open("/tmp/host",'w')
    fp.write(server_now.s_ip)
    fp.close()
    import ansible.runner
    runner=ansible.runner.Runner(
                                 host_list="/tmp/host",
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
    server_now.delete()
    return HttpResponseRedirect('/') 
def copy_sshkey(ip):
    import paramiko,os
    server=Server.objects.get(s_ip=ip)
    sshkey_path=os.path.expanduser('~/.ssh/id_rsa.pub')
    if not os.path.exists(sshkey_path):
        HttpResponse("请到服务器上生成公钥，路径为：~/.ssh/id_rsa.pub")
    ssh_key=open(sshkey_path,'r').read()
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server.s_ip, username=server.s_user, password=server.s_password,timeout=10)
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

    return render(request,'group.html',{'group_list':group_list})
def group_add(request):
    if request.method=='POST':
        form=GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/group/') 
    else:
        form=GroupForm()
    return render_to_response('group_add.html',{'form':form,}) 
def group_edit(request,id):
    group_now=Group.objects.get(id=id)
    if request.method=='POST':
        form=GroupForm(request.POST,instance=group_now)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/group/')
    else:
        form=GroupForm(instance=group_now)
    return render_to_response('group_edit.html',{'form':form,'id':id,})
def group_del(request,id):
    group_now=Group.objects.get(id=id)
    group_now.delete()
    return HttpResponseRedirect('/group/')      
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

    context={'hardware_list':hardware_list}
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
    context={'software_list':software_list}
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
    context={'server_list':server_list}
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
    context={'server_configure_list':server_configure_list,'server':server,'down_path':down_path,'upload_path':upload_path}
    return render_to_response('server_configure_manage.html',context, context_instance=RequestContext(request))

def server_configure_new(request,id):
    server=Server.objects.get(id=id)
    if request.method=="POST":
        form=ServerConfigureForm(request.POST)   
        if form.is_valid():
            serconf=ServerConfigure()
            file_name=form['ser_name'].value()
            path=MEDIA_ROOT+"/yml/server/"
            if not os.path.exists(path):
                os.makedirs(path)
            file_path=path+file_name+time.strftime('_%Y%m%d%H%M%S')+'.yml'
            dst=open(file_path,'wt')
            line='---\n- hosts: '+server.s_ip+'\n  #hosts automatic generated,not change\n'
            dst.write(line)
            dst.close()
            serconf.ser_name=file_name
            serconf.ser_path=file_path
            server.serverconfigure_set.add(serconf)
            serconf.save()
            server_configure_change(serconf.id)
            return HttpResponseRedirect('/server_configure_manage/'+str(server.id)) 
            
    else:
        form=ServerConfigureForm()
    return render_to_response('server_configure_new.html',{'form':form,'server':server}) 

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
    return render_to_response('server_configure_edit.html',{'form':form,'serconf_ser_name':serconf.ser_name,'id':id,'server_id':server_id,})

def server_configure_del(request,id):
    serconf=ServerConfigure.objects.get(id=id)
    server_id=str(serconf.ser_server.id)
    try:
        os.remove(serconf.ser_path)
    except Exception,e:
        print e
    serconf.delete()
    return HttpResponseRedirect('/server_configure_manage/'+server_id)

def server_configure_change(id):
    serconf=ServerConfigure.objects.get(id=id)
    import commands
    result=commands.getstatusoutput('ansible-playbook --syntax-check '+serconf.ser_path)
    if result[0]!=0:
        serconf.ser_status=result[1]
        serconf.save()
        return serconf.id
    serconf.ser_status='OK'
    serconf.save()
    return serconf.id
    