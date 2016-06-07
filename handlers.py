from tornado.web import RequestHandler
from tornado.web import authenticated

from models import *


class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")
    @property
    def db(self):
        return self.application.db
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
        user=self.db.query(User).filter(User.username==username).one()
        if password == user.password:
            self.set_secure_cookie("user", username)
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
        #self.write("OK")
        self.render('dashboard.html')