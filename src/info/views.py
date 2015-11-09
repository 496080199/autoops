from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from info.models import Server,Group, Hardware, Software
from info.models import ServerForm,GroupForm
from django.http.response import HttpResponseRedirect
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage

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
                hardware.h_type=ob['ansible_product_name']
                if ob['ansible_machine']=='x86_64' or ob['ansible_machine']=='x86':
                    hardware.h_cpu=ob['ansible_processor'][1]
                else:
                    hardware.h_cpu=ob['ansible_processor'][0]
                hardware.h_core=ob['ansible_processor_cores']
                hardware.h_diskmodel=''
                hardware.h_disktotal=''
                for mount in ob['ansible_mounts']:
                    hardware.h_diskmodel+=str(mount['mount'])+'\r\n'
                    size_total=float(mount['size_total'])/1024/1024/1024
                    hardware.h_disktotal+=str(float('%0.3f'%size_total))+'GB\r\n'
                hardware.h_mem=str(ob['ansible_memtotal_mb'])+'MB'

                software.so_servername=ob['ansible_distribution']
                software.so_serverrel=ob['ansible_distribution_version']
                software.so_kernel=ob['ansible_kernel']
                software.so_python=ob['ansible_python_version']

                server_now.s_status="OK"
            else:
                server_now.s_status=data['dark'][server_now.s_ip]['msg']
            
            hardware.save()
            software.save()
            server_now.save()
            
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
            
            server_now=Server.objects.get(s_ip=form['s_ip'].value())
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
                server_now.hardware_set.h_type=ob['ansible_product_name']
                if ob['ansible_machine']=='x86_64' or ob['ansible_machine']=='x86':
                    server_now.hardware_set.h_cpu=ob['ansible_processor'][1]
                else:
                    server_now.hardware_set.h_cpu=ob['ansible_processor'][0]
                server_now.hardware_set.h_core=ob['ansible_processor_cores']
                server_now.hardware_set.h_diskmodel=''
                server_now.hardware_set.h_disktotal=''
                for mount in ob['ansible_mounts']:
                    server_now.hardware_set.h_diskmodel+=str(mount['mount'])+'\r\n'
                    size_total=float(mount['size_total'])/1024/1024/1024
                    server_now.hardware_set.h_disktotal+=str(float('%0.3f'%size_total))+'GB\r\n'
                server_now.hardware_set.h_mem=str(ob['ansible_memtotal_mb'])+'MB'

                server_now.software_set.so_servername=ob['ansible_distribution']
                server_now.software_set.so_serverrel=ob['ansible_distribution_version']
                server_now.software_set.so_kernel=ob['ansible_kernel']
                server_now.software_set.so_python=ob['ansible_python_version']

                server_now.s_status="OK"
            else:
                server_now.s_status=data['dark'][server_now.s_ip]['msg']
            
            server_now.hardware_set.save()
            server_now.software_set.save()
            server_now.save()
            return HttpResponseRedirect('/') 
    else:
        form=ServerForm(instance=server_now)
    return render(request,'server_edit.html',{'form':form})
def server_del(request,ip):
    server_now=Server.objects.get(s_ip=ip)
    server_now.delete()
    return HttpResponseRedirect('/') 
    
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
