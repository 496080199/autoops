# -*- coding:utf-8 -*-  
import tornado.ioloop
from tornado.web import Application
import tornado.options
import tornado.httpserver
from handlers import *
from models import *
from tornado.web import url
from sqlalchemy.orm import scoped_session, sessionmaker
import os

from tornado.options import define,options
define("port",default=8000,help="run on the given port",type=int)

class Application(Application):
    def __init__(self):
        handlers=[
                  url(r"/",HomeHandler,name='home'),
                  url(r"/login",LoginHandler,name='login'),
                  url(r"/logout",LogoutHandler,name='logout'),
                  url(r"/dashboard",DashboardHandler,name='dashboard'),
                  url(r"/autopub",AutopubHandler,name='autopub'),
                  url(r"/env/([0-9]+)",EnvHandler,name='env'),
                  url(r"/newenv",NewenvHandler,name='newenv'),
                  url(r"/editenv/([0-9]+)",EditenvHandler,name='editenv'),
                  url(r"/delenv/([0-9]+)",DelenvHandler,name='delenv'),
                  url(r"/newprod/([0-9]+)",NewprodHandler,name='newprod'),
                  url(r"/editprod/([0-9]+)/([0-9]+)",EditprodHandler,name='editprod'),
                  url(r"/delprod/([0-9]+)/([0-9]+)",DelprodHandler,name='delprod'),
                  url(r"/conf/([0-9]+)/([0-9]+)",ConfHandler,name='conf'),
                  url(r"/message/([0-9]+)",MessageHandler,name='message'),
                  url(r"/conffile/([0-9]+)/([0-9]+)",ConffileHandler,name='conffile'),
                  url(r"/newconffile/([0-9]+)/([0-9]+)",NewconffileHandler,name='newconffile'),
                  url(r"/editconffile/([0-9]+)/([0-9]+)/([0-9]+)",EditconffileHandler,name='editconffile'),
                  url(r"/delconffile/([0-9]+)/([0-9]+)/([0-9]+)",DelconffileHandler,name='delconffile'),
                  url(r"/viewconffile/([0-9]+)/([0-9]+)/([0-9]+)",ViewconffileHandler,name='viewconffile'),
                  url(r"/ver/([0-9]+)/([0-9]+)",VerHandler,name='ver'),
                  url(r"/newver/([0-9]+)/([0-9]+)",NewverHandler,name='newver'),
                  url(r"/editver/([0-9]+)/([0-9]+)/([0-9]+)",EditverHandler,name='editver'),
                  url(r"/delver/([0-9]+)/([0-9]+)/([0-9]+)",DelverHandler,name='delver'),
                  url(r"/downver/([0-9]+)/([0-9]+)/([0-9]+)",DownverHandler,name='downver'),
                  url(r"/pubver/([0-9]+)/([0-9]+)/([0-9]+)",PubverHandler,name='pubver'),
                  url(r"/viewpublog/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)",ViewpublogHandler,name='viewpublog'),
                  url(r"/publog/([0-9]+)/([0-9]+)",PublogHandler,name='publog'),
        ]
        settings = {
        "ui_modules":{'Env': EnvModule,'Prod':ProdModule,'Conffile':ConffileModule,'Ver':VerModule},
        "template_path":os.path.join(os.path.dirname(__file__), "templates"),
        "static_path":os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "login_url": "/login",
        "xsrf_cookies": True,
        }
        tornado.web.Application.__init__(self,handlers,debug=True,**settings)
        
if __name__=="__main__":
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
