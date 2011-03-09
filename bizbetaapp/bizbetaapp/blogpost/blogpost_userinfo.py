'''
Created on May 13, 2010

@author: derek
'''
import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def get(self):
        
            user = users.get_current_user()
            if user:
                username = user.nickname()
                url = users.create_logout_url(self.request.uri)
                urltxt = "Logout"
                user.user_id()
                
            else:
                username = "nick"
                url = users.create_login_url(self.request.uri)
                urltxt = "login"

            #username = "test user"
            useremail = "test@gmail.com"

            userinfo={
                    'username': username ,
                    'useremail': useremail,
                    'url': url,
                    'urltxt': urltxt
                    }

             
             
            path = os.path.join(os.path.dirname(__file__), 'userinfo.html')
            self.response.out.write(template.render(path, userinfo))

      
application = webapp.WSGIApplication(
                                     [('/userinfo', MainPage)
                                      ],
                                     debug=True)    
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main() 