#!/usr/bin/env python
# coding=utf-8

import os
import time
import wsgiref.handlers

from v2ex.picky import Datum

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db

class MainHandler(webapp.RequestHandler):
  def get(self):
    site_domain = Datum.get('site_domain')
    site_name = Datum.get('site_name')
    site_author = Datum.get('site_author')
    site_slogan = Datum.get('site_slogan')
    site_analytics = Datum.get('site_analytics')
    site_updated = Datum.get('site_updated')
    if site_updated is None:
      site_updated = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    feed_url = Datum.get('feed_url')
    if feed_url is None:
      feed_url = '/index.xml'
    else:
      if len(feed_url) == 0:
        feed_url = '/index.xml'

    template_values = {
      'site_domain' : site_domain,
      'site_name' : site_name,
      'site_author' : site_author,
      'site_slogan' : site_slogan,
      'feed_url' : feed_url
    }

    if site_analytics is not None:
      template_values['site_analytics'] = site_analytics
    
    output = memcache.get('index_output_a')
    if output is None:
      articles = memcache.get('index')
      if articles is None:
        articles = db.GqlQuery("SELECT * FROM Article WHERE is_page = FALSE ORDER BY created DESC LIMIT 12")
        memcache.add("index", articles, 86400)
      pages = db.GqlQuery("SELECT * FROM Article WHERE is_page = TRUE AND is_for_sidebar = TRUE ORDER BY title ASC")
      template_values['page_title'] = site_name
      template_values['articles'] = articles
      template_values['articles_total'] = articles.count()
      template_values['pages'] = pages
      template_values['pages_total'] = pages.count()
      template_values['page_archive'] = False
      site_theme = Datum.get('site_theme')
      if site_theme is None:
        site_theme = 'default'
      themes = os.listdir(os.path.join(os.path.dirname(__file__), 'tpl', 'themes'))
      if site_theme not in themes:
        site_theme = 'default'
      path = os.path.join(os.path.dirname(__file__), 'tpl', 'themes', site_theme, 'index.html')
      output = template.render(path, template_values)
      memcache.set('index_output', output, 86400)
    self.response.out.write(output)

class ArchiveHandler(webapp.RequestHandler):
  def get(self):
    site_domain = Datum.get('site_domain')
    site_name = Datum.get('site_name')
    site_author = Datum.get('site_author')
    site_slogan = Datum.get('site_slogan')
    site_analytics = Datum.get('site_analytics')
    site_updated = Datum.get('site_updated')
    if site_updated is None:
      site_updated = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    feed_url = Datum.get('feed_url')
    if feed_url is None:
      feed_url = '/index.xml'
    else:
      if len(feed_url) == 0:
        feed_url = '/index.xml'

    template_values = {
      'site_domain' : site_domain,
      'site_name' : site_name,
      'site_author' : site_author,
      'site_slogan' : site_slogan,
      'feed_url' : feed_url
    }

    if site_analytics is not None:
      template_values['site_analytics'] = site_analytics
    
    output = memcache.get('archive_output')
    if output is None:  
      articles = memcache.get('archive')
      if articles is None:
        articles = db.GqlQuery("SELECT * FROM Article WHERE is_page = FALSE ORDER BY created DESC")
        memcache.add("archive", articles, 86400)
      pages = db.GqlQuery("SELECT * FROM Article WHERE is_page = TRUE AND is_for_sidebar = TRUE ORDER BY title ASC")
      if site_name is not None:
        template_values['page_title'] = site_name + ' Archive'
      else:
        template_values['page_title'] = 'Project Picky Archive'
      template_values['articles'] = articles
      template_values['articles_total'] = articles.count()
      template_values['pages'] = pages
      template_values['pages_total'] = pages.count()
      template_values['page_archive'] = True
      site_theme = Datum.get('site_theme')
      if site_theme is None:
        site_theme = 'default'
      themes = os.listdir(os.path.join(os.path.dirname(__file__), 'tpl', 'themes'))
      if site_theme not in themes:
        site_theme = 'default'
      path = os.path.join(os.path.dirname(__file__), 'tpl', 'themes', site_theme, 'index.html')
      output = template.render(path, template_values)
      memcache.add('archive_output', output, 86400)
    self.response.out.write(output)
  
class ArticleHandler(webapp.RequestHandler):
  def get(self, url):
    site_domain = Datum.get('site_domain')
    site_name = Datum.get('site_name')
    site_author = Datum.get('site_author')
    site_slogan = Datum.get('site_slogan')
    site_analytics = Datum.get('site_analytics')
    site_updated = Datum.get('site_updated')
    if site_updated is None:
      site_updated = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    feed_url = Datum.get('feed_url')
    if feed_url is None:
      feed_url = '/index.xml'
    else:
      if len(feed_url) == 0:
        feed_url = '/index.xml'

    template_values = {
      'site_domain' : site_domain,
      'site_name' : site_name,
      'site_author' : site_author,
      'site_slogan' : site_slogan,
      'feed_url' : feed_url
    }

    if site_analytics is not None:
      template_values['site_analytics'] = site_analytics
    
    pages = db.GqlQuery("SELECT * FROM Article WHERE is_page = TRUE AND is_for_sidebar = TRUE ORDER BY title ASC")
    article = db.GqlQuery("SELECT * FROM Article WHERE title_url = :1 LIMIT 1", url)
    if (article.count() == 1):
      article_found = True
      article = article[0]
      article.hits = article.hits + 1
      try:
        article.put()
      except:
        article.hits = article.hits - 1
    else:
      article_found = False
    if (article_found):
      parent = None
      if article.parent is not '':
        q = db.GqlQuery("SELECT * FROM Article WHERE title_url = :1 LIMIT 1", article.parent_url)
        if q.count() == 1:
          parent = q[0]
      template_values['parent'] = parent
      template_values['page_title'] = article.title
      template_values['article'] = article
      template_values['pages'] = pages
      template_values['pages_total'] = pages.count()
      site_theme = Datum.get('site_theme')
      if site_theme is None:
        site_theme = 'default'
      themes = os.listdir(os.path.join(os.path.dirname(__file__), 'tpl', 'themes'))
      if site_theme not in themes:
        site_theme = 'default'
      path = os.path.join(os.path.dirname(__file__), 'tpl', 'themes', site_theme, 'article.html')
      self.response.out.write(template.render(path, template_values))
    else:
      template_values['page_title'] = 'Project Picky › Article Not Found'
      template_values['pages'] = pages
      template_values['pages_total'] = pages.count()
      site_theme = Datum.get('site_theme')
      if site_theme is None:
        site_theme = 'default'
      themes = os.listdir(os.path.join(os.path.dirname(__file__), 'tpl', 'themes'))
      if site_theme not in themes:
        site_theme = 'default'
      path = os.path.join(os.path.dirname(__file__), 'tpl', 'themes', site_theme, '404.html')
      self.response.out.write(template.render(path, template_values))

class AtomFeedHandler(webapp.RequestHandler):
  def get(self):
    site_domain = Datum.get('site_domain')
    site_name = Datum.get('site_name')
    site_author = Datum.get('site_author')
    site_slogan = Datum.get('site_slogan')
    site_analytics = Datum.get('site_analytics')
    site_updated = Datum.get('site_updated')
    if site_updated is None:
      site_updated = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    feed_url = Datum.get('feed_url')
    if feed_url is None:
      feed_url = '/index.xml'
    else:
      if len(feed_url) == 0:
        feed_url = '/index.xml'

    template_values = {
      'site_domain' : site_domain,
      'site_name' : site_name,
      'site_author' : site_author,
      'site_slogan' : site_slogan,
      'feed_url' : feed_url
    }

    if site_analytics is not None:
      template_values['site_analytics'] = site_analytics
    
    output = memcache.get('feed_output')
    if output is None:
      articles = db.GqlQuery("SELECT * FROM Article WHERE is_page = FALSE ORDER BY created DESC LIMIT 100")
      template_values['articles'] = articles
      template_values['articles_total'] = articles.count()
      template_values['site_updated'] = site_updated
      path = os.path.join(os.path.dirname(__file__), 'tpl', 'shared', 'index.xml')
      output = template.render(path, template_values)
      memcache.set('feed_output', output, 86400)
    self.response.headers['Content-type'] = 'text/xml; charset=UTF-8'
    self.response.out.write(output)

class AtomSitemapHandler(webapp.RequestHandler):
  def get(self):
    site_domain = Datum.get('site_domain')
    site_name = Datum.get('site_name')
    site_author = Datum.get('site_author')
    site_slogan = Datum.get('site_slogan')
    site_analytics = Datum.get('site_analytics')
    site_updated = Datum.get('site_updated')
    if site_updated is None:
      site_updated = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    feed_url = Datum.get('feed_url')
    if feed_url is None:
      feed_url = '/index.xml'
    else:
      if len(feed_url) == 0:
        feed_url = '/index.xml'

    template_values = {
      'site_domain' : site_domain,
      'site_name' : site_name,
      'site_author' : site_author,
      'site_slogan' : site_slogan,
      'feed_url' : feed_url
    }

    if site_analytics is not None:
      template_values['site_analytics'] = site_analytics
    
    output = memcache.get('sitemap_output')
    if output is None:
      articles = db.GqlQuery("SELECT * FROM Article ORDER BY last_modified DESC")
      template_values['articles'] = articles
      template_values['articles_total'] = articles.count()
      template_values['site_updated'] = site_updated
      path = os.path.join(os.path.dirname(__file__), 'tpl', 'shared', 'sitemap.xml')
      output = template.render(path, template_values)
      memcache.set('sitemap_output', output, 86400)
    self.response.headers['Content-type'] = 'text/xml; charset=UTF-8'
    self.response.out.write(output)
    
class RobotsHandler(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'tpl', 'shared', 'robots.txt')
    self.response.headers['Content-type'] = 'text/plain; charset=UTF-8'
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([
  ('/archive', ArchiveHandler),
  ('/index.xml', AtomFeedHandler),
  ('/sitemap.xml', AtomSitemapHandler),
  ('/robots.txt', RobotsHandler),
  ('/', MainHandler),
  ('/([0-9a-zA-Z\-\.]+)', ArticleHandler)
  ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()