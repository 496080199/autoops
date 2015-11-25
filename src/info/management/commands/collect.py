# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from info.models import * 
import time,paramiko
#import MySQLdb
#import ansible.runner
from ljcms.settings import DATABASES, MEDIA_ROOT


class Command(BaseCommand):
    def handle(self, *args, **options):
        while 1: 
            servers=Server.objects.all()
            for server in servers:
                if server.s_monitor==True:
                    log=Log(server=server)
                    log.save()
                    path=MEDIA_ROOT+'/server_inv.py' 
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(server.s_ip,server.s_port,server.s_user, server.s_password)
                    ssh.exec_command('yum install -y sysstat')
                    ##IO##
                    stdin,stdout,stderr=ssh.exec_command('sar -dp 1 2|grep -E "Average|平均时间" |grep -v DEV')
                    out=stdout.read()
                    sar_iolist=out.split('\n')
                    io={}
                    for sar_io in sar_iolist:
                        line=sar_io.split('      ')
                        if len(line)==10:
                            io[line[1]]=[line[2],line[3],line[4],line[9]]
                    for key in io:
                        log_io=Io(log=log)
                        log_io.dev=key
                        log_io.tps=io[key][0]
                        log_io.rd_sec=io[key][1]
                        log_io.wd_sec=io[key][2]
                        log_io.util=io[key][3]
                        log_io.save()
                        
                    ssh.close()
                        
                    
                    
            time.sleep(300)       

            

            