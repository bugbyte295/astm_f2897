#!/usr/bin/python
# -*- coding: utf-8 -*-
        
import cherrypy
import urllib3
import requests
import astm_f2897
import json
    
scans = []
url = "https://hooks.airtable.com/workflows/v1/genericWebhook/appyXNoDQSrFR8sIS/wfl8yyvj4U7k9RlME/wtrSYdGh47sPP8Fnu"
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
    data = astm_f2897.main(content)
    x = requests.post(url,dict(data))
    print(x)
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
