# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from info.models import * 
import time,paramiko,re



class Command(BaseCommand):
    def handle(self, *args, **options):
        while 1: 
            servers=Server.objects.all()
            for server in servers:
                if server.s_monitor==True:
                    log=Log(server=server)
                    log.save()
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        ssh.connect(server.s_ip,server.s_port,server.s_user, server.s_password)
                    except Exception:
                        continue
                    if server.software.so_servername=='Debian':
                        ssh.exec_command('apt-get install -y sysstat')
                    else:
                        ssh.exec_command('yum install -y sysstat')
                    ##Load##
                    stdin,stdout,stderr=ssh.exec_command('sar -q 1 2|grep -E "Average|平均时间"')
                    out=stdout.read()
                    sar_list=out.split('\n')
                    for sar in sar_list:
                        line=re.split(r'\s+',sar)
                        if len(line)>1:
                            log_load=Load(log=log)
                            log_load.ldavg1=line[3]
                            log_load.ldavg5=line[4]
                            log_load.ldavg10=line[5]
                            log_load.save()

                    ##CPU##
                    stdin,stdout,stderr=ssh.exec_command('sar -u 1 2|grep -E "Average|平均时间"')
                    out=stdout.read()
                    sar_list=out.split('\n')
                    cpu={}
                    for sar in sar_list:
                        line=re.split(r'\s+',sar)
                        if len(line)>1:
                            cpu[line[1]]=[line[2],line[3],line[4],line[5],line[6],line[7]]
                    for key in cpu:
                        log_cpu=Cpu(log=log)
                        log_cpu.dev=key
                        log_cpu.user=cpu[key][0]
                        log_cpu.nice=cpu[key][1]
                        log_cpu.system=cpu[key][2]
                        log_cpu.iowait=cpu[key][3]
                        log_cpu.steal=cpu[key][4]
                        log_cpu.idle=cpu[key][5]
                        log_cpu.save()
                    ##Mem##
                    stdin,stdout,stderr=ssh.exec_command('sar -r 1 2|grep -E "Average|平均时间"')
                    out=stdout.read()
                    sar_list=out.split('\n')
                    for sar in sar_list:
                        line=re.split(r'\s+',sar)
                        if len(line)>1:
                            log_mem=Mem(log=log)
                            log_mem.kbmemfree=str(float(line[1])/1024/1024)
                            log_mem.kbmemused=str(float(line[2])/1024/1024)
                            log_mem.memused=line[3]
                            log_mem.save()
                    ##Disk##
                    stdin,stdout,stderr=ssh.exec_command('df -h |grep -Ev "Filesystem|文件系统"')
                    out=stdout.read()
                    sar_list=out.split('\n')
                    disk={}
    
                    for sar in sar_list:
                        line=re.split(r'\s+',sar)
                        if len(line)>1:
                            #log_disk=Disk(log=log)
                            #log_disk.mount=line[5]
                            #log_disk.save()
                            #disk_detail=DiskDetail(disk=log_disk)
                            #disk_detail.used=line[2]
                            #disk_detail.avail=line[3]
                            #disk_detail.use=line[4]
                            #disk_detail.save()
                            
                            
                            
                            disk[line[5]]=[line[2],line[3],line[4]]
                    log_disk=Disk(log=log)
                    for key in disk:
                        log_disk=Disk(log=log)
                        log_disk.mount=key
                        if disk[key][0].endswith('G'):
                            log_disk.used=disk[key][0].split('G')[0]
                        elif disk[key][0].endswith('M'):
                            log_disk.used=str(float(disk[key][0].split('M')[0])/1024)
                        elif disk[key][0].endswith('K'):
                            log_disk.used=str(float(disk[key][0].split('K')[0])/1024/1024)
                        else:
                            log_disk.used=str(float(disk[key][0])/1024/1024/1024)
                        if disk[key][1].endswith('G'):
                            log_disk.avail=disk[key][1].split('G')[0]
                        elif disk[key][1].endswith('M'):
                            log_disk.avail=str(float(disk[key][1].split('M')[0])/1024)
                        elif disk[key][1].endswith('K'):
                            log_disk.avail=str(float(disk[key][1].split('K')[0])/1024/1024)
                        else:
                            log_disk.avail=str(float(disk[key][1])/1024/1024/1024)
                        
                        log_disk.use=disk[key][2].split('%')[0]
                        #log_disk.use=disk[key][3]
                        # log_disk.mount=disk[key][4]
                        log_disk.save()
                    ##IO##
                    stdin,stdout,stderr=ssh.exec_command('sar -dp 1 2|grep -E "Average|平均时间" |grep -v DEV')
                    out=stdout.read()
                    sar_list=out.split('\n')
                    io={}
                    for sar in sar_list:
                        line=re.split(r'\s+',sar)
                        if len(line)>1:
                            io[line[1]]=[line[2],line[3],line[4],line[9]]
                    for key in io:
                        log_io=Io(log=log)
                        log_io.dev=key
                        log_io.tps=io[key][0]
                        log_io.rd_sec=io[key][1]
                        log_io.wd_sec=io[key][2]
                        log_io.util=io[key][3]
                        log_io.save()
                    ##Network##
                    stdin,stdout,stderr=ssh.exec_command('sar -n DEV 1 2|grep -E "Average|平均时间"|grep -v IFACE|grep -v lo')
                    out=stdout.read()
                    sar_list=out.split('\n')
                    network={}
                    for sar in sar_list:
                        line=re.split(r'\s+',sar)
                        if len(line)>1:
                            network[line[1]]=[line[2],line[3],line[4],line[5]]
                    for key in network:
                        log_network=Network(log=log)
                        log_network.dev=key
                        log_network.rxpck=network[key][0]
                        log_network.txpck=network[key][1]
                        log_network.rxbyt=str(float(network[key][2])/1024)
                        log_network.txbyt=str(float(network[key][3])/1024)
                        log_network.save() 
                    ssh.close()
                        
                    
                    
            time.sleep(300)       

            

            