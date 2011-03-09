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

class Posting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  
class MainPage(webapp.RequestHandler):
  def get(self):
    greetings_query = Posting.all().order('-date')
    postings = greetings_query.fetch(10)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'posting': postings,
      'url': url,
      'url_linktext': url_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), 'blogpost.html')
    self.response.out.write(template.render(path, template_values))
    
  
class Postbook(webapp.RequestHandler):
  def post(self):
    posting = Posting()

    if users.get_current_user():
      posting.author = users.get_current_user()

    posting.content = self.request.get('content')
    posting.put()
    self.redirect('/blogpost')  
    
    
application = webapp.WSGIApplication(
                                     [('/blogpost', MainPage),
                                      ('/blogpostsign', Postbook)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()    
    