#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
import tornado.log
import os

from jinja2 import \
  Environment, PackageLoader, select_autoescape

ENV = Environment(
  loader=PackageLoader('myapp', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))
class MainHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("hello.html", {'name': 'World'})
 
def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    # (r"/post/(.*)/comment", CommentHandler),
    # (r"/post/(.*)", BlogPostHandler),
    (r"/static/(.*)", 
      tornado.web.StaticFileHandler, {'path': 'static'}),
  ], autoreload=True)
    
if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '4444')))
  tornado.ioloop.IOLoop.current().start()