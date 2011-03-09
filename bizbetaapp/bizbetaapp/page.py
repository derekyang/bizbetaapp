#!/usr/bin/env python
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


class AboutHandler(webapp.RequestHandler):
    def get(self):
        output = " All about about test "
        self.response.out.write(output)

def main():
    application = webapp.WSGIApplication([
        ('/about',AboutHandler),
        ],                      debug = True)

    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
