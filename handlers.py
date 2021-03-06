# -*- coding:utf-8 -*-  
from tornado.web import RequestHandler
from tornado.web import authenticated
from tornado.web import asynchronous
from tornado.gen import coroutine
from datetime import datetime
from models import *
from modules import *
import os,commands,re,time,sys
from subprocess import Popen,PIPE
from crontab import CronTab

reload(sys)
sys.setdefaultencoding('utf-8')



class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")
    def initialize(self):
        self.session = DB_Session()
    def on_finish(self):
        self.session.close()
class HomeHandler(BaseHandler): 
    def get(self):
        if not self.current_user:
            self.redirect("login")       
        self.redirect("dashboard")
class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')
    def post(self):
        username=self.get_argument('username')
        password=self.get_argument('password')
        user=self.session.query(User).filter(User.username==username).one()
        if password == user.password:
            self.set_secure_cookie("user", username,expires=time.time()+2700)
            self.redirect('dashboard')
        else:
            self.redirect("login")
        
class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user",'')
        self.redirect("login")
        
class DashboardHandler(BaseHandler):
    @authenticated
    def get(self):
        status,output=commands.getstatusoutput('cat ~/.ssh/id_rsa.pub')
        regex=ur"ssh-rsa"
        if re.search(regex,output):
            content=output
        else:
            content='未找到公钥，请在服务器上使用ssh-keygen -t rsa命令生成.'
        self.render('dashboard.html',content=content)
class AutopubHandler(BaseHandler):
    @authenticated
    def get(self):
        envs=self.session.query(Env).all()
        self.render('autopub.html',envs=envs)
class EnvHandler(BaseHandler):
    @authenticated
    def get(self,env_id,class_id):
        env=self.session.query(Env).get(env_id)
        all_prods=self.session.query(Prod).filter(Prod.env_id==env_id)
        classids=[]
        for prod in all_prods:
            classids.append(prod.class_id)
        classids=list(set(classids))
        classes=[]
        for classid in classids:
            classify=self.session.query(Class).get(classid)
            classes.append(classify)
        if int(class_id) == 0:
            prods=self.session.query(Prod).filter(Prod.env_id==env_id)
        else:
            prods=self.session.query(Prod).filter(Prod.env_id==env_id).filter(Prod.class_id==class_id)

        self.render('env.html',prods=prods,env=env,classes=classes)
    
 
class EnvClassHandler(BaseHandler):
    @authenticated
    def get(self,id,class_id):
        env=self.session.query(Env).get(id)
        prods=self.session.query(Prod).filter(Prod.env_id==id).filter(Prod.class_id==class_id)
        classes=self.session.query(Class).all()
        self.render('env.html',prods=prods,env=env,classes=classes)        
class NewenvHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('newenv.html')
    @authenticated  
    def post(self):
        name=self.get_argument('name')
        env=Env(name=name)
        self.session.add(env)
        self.session.commit()
        self.redirect("/autopub")
class EditenvHandler(BaseHandler):
    @authenticated
    def get(self,id):
        env=self.session.query(Env).get(id)
        self.render('editenv.html',env=env)
    def post(self,id):
        name=self.get_argument('name')
        env=self.session.query(Env).get(id)
        env.name=name
        self.session.commit()
        self.redirect("/autopub")
class DelenvHandler(BaseHandler):
    @authenticated
    def get(self,id):
        env=self.session.query(Env).get(id)
        self.session.delete(env)
        self.session.commit()
        self.redirect("/autopub")
class ClassHandler(BaseHandler):
    @authenticated
    def get(self):
        classes=self.session.query(Class).filter(Class.id!=0)
        self.render('class.html',classes=classes)
class NewclassHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('newclass.html')
    @authenticated
    def post(self):
        name=self.get_argument('name')
        classify=Class(name=name)
        self.session.add(classify)
        self.session.commit()
        self.redirect("/class")
class EditclassHandler(BaseHandler):
    @authenticated
    def get(self,class_id):
        classify=self.session.query(Class).get(class_id)
        self.render('editclass.html',classify=classify)
    @authenticated  
    def post(self,class_id):
        name=self.get_argument('name')
        classify=self.session.query(Class).get(class_id)
        classify.name=name
        self.session.commit()
        self.redirect("/class")
class DelclassHandler(BaseHandler):
    @authenticated  
    def get(self,class_id):
        classify=self.session.query(Class).get(class_id)
        prods=self.session.query(Prod).filter(Prod.class_id==class_id)
        for prod in prods:
            prod.class_id=1
            self.session.commit()
        self.session.delete(classify)
        self.session.commit()
        self.redirect("/class")
class SetclassHandler(BaseHandler):
    @authenticated  
    def get(self,env_id,prod_id):
        classes=self.session.query(Class).all()
        prod=self.session.query(Prod).get(prod_id)
        self.render('setclass.html',env_id=env_id,prod=prod,classes=classes)
    @authenticated
    def post(self,env_id,prod_id):
        class_id=self.get_argument('class_id')
        prod=self.session.query(Prod).get(prod_id)
        prod.class_id=int(class_id)
        self.session.commit()
        self.redirect("/env/"+env_id+'/0')
class NewprodHandler(BaseHandler):
    @authenticated
    def get(self,env_id):
        self.render('newprod.html',env_id=env_id)
    @authenticated  
    def post(self,env_id):
        name=self.get_argument('name')
        prod=Prod(name=name,env_id=env_id)
        self.session.add(prod)
        self.session.commit()
        conf=Conf(prod_id=prod.id)
        self.session.add(conf)
        self.session.commit()
        self.redirect("/env/"+env_id+'/0')
class EditprodHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id):
        prod=self.session.query(Prod).get(prod_id)
        self.render('editprod.html',env_id=env_id,prod=prod)
    @authenticated  
    def post(self,env_id,prod_id):
        name=self.get_argument('name')
        prod=self.session.query(Prod).get(prod_id)
        prod.name=name
        self.session.commit()
        self.redirect("/env/"+env_id+'/0')
class DelprodHandler(BaseHandler):
    @authenticated  
    def get(self,env_id,prod_id):
        prod=self.session.query(Prod).get(prod_id)
        conf=self.session.query(Conf).filter(Conf.prod_id==prod_id).one()
        self.session.delete(conf)
        self.session.delete(prod)
        self.session.commit()
        self.redirect("/env/"+env_id+'/0')
class ConfHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id):
        env=self.session.query(Env).get(env_id)
        prod=self.session.query(Prod).get(prod_id)
        conf=self.session.query(Conf).filter(Conf.prod_id==prod_id).one()
        conffiles=self.session.query(Conffile).filter(Conffile.prod_id==prod_id)
        self.render('conf.html',env=env,prod=prod,conf=conf,conffiles=conffiles)
    @authenticated
    def post(self,env_id,prod_id): 
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        log_path=os.path.join(upload_path,'cronlogs')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        rulespath=os.path.join(upload_path,prod_id+'.yml')
        hostspath=os.path.join(upload_path,prod_id+'.host')
        conf=self.session.query(Conf).filter(Conf.prod_id==prod_id).one()
        conf.rules=self.get_argument('rules')
        rules=open(rulespath,'wb')
        rules.write(conf.rules)
        rules.close()
        conf.hosts=self.get_argument('hosts')
        hosts=open(hostspath,'wb')
        hosts.write(conf.hosts)
        hosts.close()
        conf.fetch=self.get_argument('fetch')
        conf.host=self.get_argument('host')
        conf.src=self.get_argument('src')
        self.session.commit()
        
        self.redirect("/env/"+env_id+'/0')
class MessageHandler(BaseHandler):
    @authenticated
    def get(self,id):
        self.render('message.html',id=id)
class ConffileHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id):
        env=self.session.query(Env).get(env_id)
        prod=self.session.query(Prod).get(prod_id)
        conffiles=self.session.query(Conffile).filter(Conffile.prod_id==prod_id)
        self.render('conffile.html',env=env,prod=prod,conffiles=conffiles)
class NewconffileHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id):
        self.render('newconffile.html',env_id=env_id,prod_id=prod_id)
    @authenticated
    def post(self,env_id,prod_id):
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        if self.request.files.has_key('file'): 
            file_metas=self.request.files['file']
            for meta in file_metas:
                filename=meta['filename']
            filepath=os.path.join(upload_path,filename)
            if not os.path.exists(filepath):
                with open(filepath,'wb') as up:
                    up.write(meta['body'])
                conffile=Conffile(name=filename,prod_id=prod_id,file=filename)
                self.session.add(conffile)
                self.session.commit()
                self.redirect("/conffile/"+env_id+'/'+prod_id)
            else:
                self.redirect("/message/1")
        else:
            self.redirect("/message/2")
class EditconffileHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id,conffile_id):
        conffile=self.session.query(Conffile).get(conffile_id)
        self.render('editconffile.html',env_id=env_id,prod_id=prod_id,conffile=conffile)
    @authenticated   
    def post(self,env_id,prod_id,conffile_id):
        conffile=self.session.query(Conffile).get(conffile_id)
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        if self.request.files.has_key('file'):            
            file_metas=self.request.files['file']
            for meta in file_metas:
                filename=conffile.file
                filepath=os.path.join(upload_path,filename)         
                with open(filepath,'wb') as up:
                    up.write(meta['body'])
            conffile.time=datetime.now()
            self.session.commit()
            self.redirect("/conffile/"+env_id+'/'+prod_id)
        else:
            self.redirect("/message/2")
class DelconffileHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id,conffile_id):
        conffile=self.session.query(Conffile).get(conffile_id)
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        filepath=os.path.join(upload_path,conffile.file)
        if os.path.exists(filepath):
            os.remove(filepath)
        self.session.delete(conffile)
        self.session.commit()
        self.redirect("/conffile/"+env_id+'/'+prod_id)
class ViewconffileHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id,conffile_id):
        conffile=self.session.query(Conffile).get(conffile_id)
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        filepath=os.path.join(upload_path,conffile.file)
        file = open(filepath, 'rb')
        content=file.read()
        self.render('viewconffile.html',env_id=env_id,prod_id=prod_id,conffile=conffile,content=content)
    @authenticated
    def post(self,env_id,prod_id,conffile_id):
        content=self.get_argument("content")
        conffile=self.session.query(Conffile).get(conffile_id)
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        filepath=os.path.join(upload_path,conffile.file)
        file=open(filepath, 'wb')
        file.write(content)
        file.close()
        conffile.time=datetime.now()
        self.session.commit()
        self.redirect("/conffile/"+env_id+'/'+prod_id)
class VerHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id,maj_id):
        env=self.session.query(Env).get(env_id)
        prod=self.session.query(Prod).get(prod_id)
        all_vers=self.session.query(Ver).filter(Ver.prod_id==prod_id) 
        majs=[]
        for ver in all_vers:
            majs.append(ver.major)
        majs=list(set(majs))
        if int(maj_id) == 0:
            vers=self.session.query(Ver).filter(Ver.prod_id==prod_id).order_by(desc(Ver.pub_time))
        else:
            vers=self.session.query(Ver).filter(Ver.prod_id==prod_id).filter(Ver.major==maj_id).order_by(desc(Ver.pub_time)) 
        self.render('ver.html',env=env,prod=prod,vers=vers,majs=majs)
class ImportverHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id):
        conf=self.session.query(Conf).filter(Conf.prod_id==prod_id).one()
        if conf.fetch == 1:
            time=datetime.now().strftime("%Y%m%d%H%M%S")
            major=int(datetime.now().strftime("%Y%m"))
            files_path=os.path.join(os.path.dirname(__file__),'files/')
            upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
            dest=upload_path+"/"+time+".pak"
            status,output=commands.getstatusoutput("cd "+files_path+"&&ansible-playbook fetch.yml -i hosts -e \"host="+conf.host+" src="+conf.src+" dest="+dest+"\" ")
            if int(status) == 0:
                ver=Ver(name=time,major=major,minor=0,revison=0,file=time+".pak",prod_id=prod_id,pub_time=datetime.now(),ch_time=datetime.now())
                self.session.add(ver)
                self.session.commit()
                timepub=Timepub(ver_id=ver.id)
                self.session.add(timepub)
                self.session.commit()
            self.redirect("/ver/"+env_id+'/'+prod_id+'/0')
        else:
            self.redirect("/message/3")
class NewverHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id):
        self.render('newver.html',env_id=env_id,prod_id=prod_id)
    @authenticated
    def post(self,env_id,prod_id):
        major=self.get_argument("major")
        minor=self.get_argument("minor")
        revison=self.get_argument("revison")
        name="V"+major+"."+minor+"."+revison
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        if self.request.files.has_key('file'):
            file_metas=self.request.files['file']
            for meta in file_metas:
                filename=name+'_'+meta['filename']
            filepath=os.path.join(upload_path,filename)
            if not os.path.exists(filepath):
                with open(filepath,'wb') as up:
                    up.write(meta['body'])
                ver=Ver(name=name,major=major,minor=minor,revison=revison,file=filename,prod_id=prod_id,pub_time=datetime.now(),ch_time=datetime.now())
                self.session.add(ver)
                self.session.commit()
                timepub=Timepub(ver_id=ver.id)
                self.session.add(timepub)
                self.session.commit()
                self.redirect("/ver/"+env_id+'/'+prod_id+'/0')
            else:
                self.redirect("/message/1")
        else:
            self.redirect("/message/2")
            
class EditverHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id,ver_id):
        ver=self.session.query(Ver).get(ver_id)
        self.render('editver.html',env_id=env_id,prod_id=prod_id,ver=ver)
    @authenticated   
    def post(self,env_id,prod_id,ver_id):
        ver=self.session.query(Ver).get(ver_id)
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        if self.request.files.has_key('file'):
            file_metas=self.request.files['file']
            for meta in file_metas:
                filename=ver.name+'_'+meta['filename']
            filepath=os.path.join(upload_path,filename)         
            with open(filepath,'wb') as up:
                up.write(meta['body'])
            ver.file=filename
            ver.ch_time=datetime.now()
            self.session.commit()
            self.redirect("/ver/"+env_id+'/'+prod_id+'/0') 
        else:
            self.redirect("/message/2")
class DelverHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id,ver_id):
        ver=self.session.query(Ver).get(ver_id)
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        filepath=os.path.join(upload_path,ver.file)
        if os.path.exists(filepath):
            os.remove(filepath)
        user_cron=CronTab(user=True) 
        iter = user_cron.find_comment('autoops_'+ver.name+'_'+ver_id)
        for job in iter:
            user_cron.remove(job)
        user_cron.write_to_user(user=True) 
        timepub=self.session.query(Timepub).filter(Timepub.ver_id==ver_id).one()
        self.session.delete(timepub)
        self.session.commit()
        self.session.delete(ver)
        self.session.commit()
        self.redirect("/ver/"+env_id+'/'+prod_id+'/0')  
class DownverHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id,ver_id):
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        ver=self.session.query(Ver).get(ver_id)
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename='+ver.file)
        filepath=os.path.join(upload_path,ver.file)
        with open(filepath, 'rb') as f:
            while True:
                data = f.read()
                if not data:
                    break
                self.write(data)
                
        self.finish()
class CheckHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id,ver_id):
        ver=self.session.query(Ver).get(ver_id)
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)     
        popen=Popen("cd "+upload_path+"&&ansible-playbook "+prod_id+".yml -i "+prod_id+".host -e \"ver="+ver.file+"\" --syntax-check",shell=True,stdout=PIPE)
        popen.wait()
        content=popen.stdout.read()
        self.render('check.html',content=content)
class PubverHandler(BaseHandler): 
    @authenticated
    def get(self,env_id,prod_id,ver_id):
        ver=self.session.query(Ver).get(ver_id)
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        log_path=os.path.join(upload_path,'logs/')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        publog=Publog(prod_id=prod_id,user=self.get_current_user(),time=datetime.now(),log=u'发布了'+ver.name,content='')
        self.session.add(publog)
        self.session.commit()        
        popen=Popen("cd "+upload_path+"&&ansible-playbook "+prod_id+".yml -i "+prod_id+".host -e \"ver="+ver.file+"\" | tee "+log_path+str(publog.id)+".log",shell=True)
        #status,output=commands.getstatusoutput('cd '+upload_path+'&&ansible-playbook '+prod_id+'.yml -i '+prod_id+'.host -e "bag='+ver.file+'"')
        self.redirect("/viewpublog/"+env_id+'/'+prod_id+'/'+str(publog.id))
class TimepubHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id,ver_id):
        timepub=self.session.query(Timepub).filter(Timepub.ver_id==ver_id).one()
        self.render('timepub.html',env_id=env_id,prod_id=prod_id,ver_id=ver_id,timepub=timepub) 
    @authenticated
    def post(self,env_id,prod_id,ver_id):
        user_cron=CronTab(user=True) 
        timepub=self.session.query(Timepub).filter(Timepub.ver_id==ver_id).one()
        timepub.time=self.get_argument('time')
        timepub.min=self.get_argument('min')
        timepub.hour=self.get_argument('hour')
        timepub.day=self.get_argument('day')
        timepub.mon=self.get_argument('mon')
        timepub.week=self.get_argument('week')
        self.session.commit()
        ver=self.session.query(Ver).get(ver_id)
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        if int(timepub.time) == 1:
            iter = user_cron.find_comment('autoops_'+ver.name+'_'+ver_id)
            for job in iter:
                if job:
                    user_cron.remove(job)
                    user_cron.write_to_user(user=True)
            job = user_cron.new(command="cd "+upload_path+"&&ansible-playbook "+prod_id+".yml -i "+prod_id+".host -e \"ver="+ver.file+"\" | tee cronlogs/cron_"+ver.name+"_$(date +\%Y\%m\%d\%H\%M\%S).log", comment='autoops_'+ver.name+'_'+ver_id)
            job.setall(timepub.min+' '+timepub.hour+' '+timepub.day+' '+timepub.mon+' '+timepub.week)
            job.enable()
            user_cron.write_to_user(user=True)
        else:
            iter = user_cron.find_comment('autoops_'+ver.name+'_'+ver_id)
            for job in iter:
                user_cron.remove(job)
            user_cron.write_to_user(user=True) 
        self.redirect("/ver/"+env_id+'/'+prod_id+'/0')
class ViewpublogHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id,publog_id):
        publog=self.session.query(Publog).get(publog_id)
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        log_path=os.path.join(upload_path,'logs/'+publog_id+'.log')
        if os.path.exists(log_path):
            logfile=open(log_path,'rb')
            publog.content=logfile.read()
            self.session.commit()
            logfile.close()
        self.render('viewpublog.html',publog=publog)
        
class PublogHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id):
        env=self.session.query(Env).get(env_id)
        prod=self.session.query(Prod).get(prod_id)
        publogs=self.session.query(Publog).filter(Publog.prod_id==prod_id).order_by(desc(Publog.time)).limit(50)
        self.render('publog.html',publogs=publogs,env=env,prod=prod)
class CronlogHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id):
        env=self.session.query(Env).get(env_id)
        prod=self.session.query(Prod).get(prod_id)
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        log_path=os.path.join(upload_path,'cronlogs')
        crons=os.listdir(log_path)
        crons.sort()
        self.render('cronlog.html',env=env,prod=prod,crons=crons)
class ViewcronlogHandler(BaseHandler):
    @authenticated
    def get(self,env_id,prod_id,log_name):
        upload_path=os.path.join(os.path.dirname(__file__),'files/'+env_id+'/'+prod_id)
        log_path=os.path.join(upload_path,'cronlogs')
        log_file=open(log_path+'/'+log_name,'rb')
        content=log_file.read()
        self.render('viewcronlog.html',content=content)
    
        
        
        
    
    