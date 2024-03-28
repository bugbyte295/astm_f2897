#!/usr/bin/python
# -*- coding: utf-8 -*-
        
import cherrypy
import urllib
    
scans = []

class Scans:
        
  exposed = True
        
  def GET(self):
    return ('Here are all the scans: %s' % scans)
        
  def POST(self, **kwargs):
    # cherrypy.response.status = 404
    # cherrypy.response.headers['Custom-Title'] = urllib.parse.quote_plus('My custom error')
    # cherrypy.response.headers['Custom-Message'] = urllib.parse.quote_plus('The record already exists.')
                
    # in ms, if not set automatic time depending on the length, 0 = forever
    cherrypy.response.headers['Custom-Time'] = '5000'
        
    content = "unknown content"
    format = "unknown format"
        
    if "content" in kwargs:
        content = kwargs["content"]
    if "format" in kwargs:
        format = kwargs["format"]
        
    scans.append((content, format))
    return ('Append new scan with content: %s, format %s' % (content, format))
        
if __name__ == '__main__':
        
  conf = {
  'global': {
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080
  },
  '/': {
    'request.dispatch': cherrypy.dispatch.MethodDispatcher()
  }
  }
        
  cherrypy.quickstart(Scans(), '/scans/', conf)