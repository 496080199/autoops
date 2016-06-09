# -*- coding:utf-8 -*-  
from tornado.web import UIModule

class EnvModule(UIModule):
    def render(self,env):
        return self.render_string('modules/env.html',env=env)

