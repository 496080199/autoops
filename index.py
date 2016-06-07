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
                  url(r"/dashboard",DashboardHandler,name='dashboard')
        ]
        settings = {
        "template_path":os.path.join(os.path.dirname(__file__), "templates"),
        "static_path":os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "login_url": "/login",
        "xsrf_cookies": True,
        }
        tornado.web.Application.__init__(self,handlers,debug=True,**settings)
        self.db = scoped_session(sessionmaker(bind=engine))
if __name__=="__main__":
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
