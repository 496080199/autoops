# -*- coding:utf-8 -*-  
from tornado.web import UIModule

class EnvModule(UIModule):
    def render(self,env):
        return self.render_string('modules/env.html',env=env)
class ProdModule(UIModule):
    def render(self,prod,env):
        return self.render_string('modules/prod.html',prod=prod,env=env)

