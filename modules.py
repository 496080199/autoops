# -*- coding:utf-8 -*-  
from tornado.web import UIModule

class EnvModule(UIModule):
    def render(self,env):
        return self.render_string('modules/env.html',env=env)
class ProdModule(UIModule):
    def render(self,prod,env):
        return self.render_string('modules/prod.html',prod=prod,env=env)
class ConffileModule(UIModule):
    def render(self,prod,env,conffile):
        return self.render_string('modules/conffile.html',prod=prod,env=env,conffile=conffile)

