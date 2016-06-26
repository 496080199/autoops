# -*- coding:utf-8 -*-  
from tornado.web import UIModule

class EnvModule(UIModule):
    def render(self,env):
        return self.render_string('modules/env.html',env=env)
class ClassModule(UIModule):
    def render(self,classify):
        return self.render_string('modules/class.html',classify=classify)
class ProdModule(UIModule):
    def render(self,prod,env):
        return self.render_string('modules/prod.html',prod=prod,env=env)
class ConffileModule(UIModule):
    def render(self,prod,env,conffile):
        return self.render_string('modules/conffile.html',prod=prod,env=env,conffile=conffile)
class VerModule(UIModule):
    def render(self,prod,env,ver):
        return self.render_string('modules/ver.html',prod=prod,env=env,ver=ver)
    

