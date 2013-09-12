#!/usr/bin/env python
from paste.translogger import Translogger

def application( environ, start_response ):
  status = '200 OK'
  response_headers = [('Content-type', 'text/plain')]
  start_response( status,  response_headers )
  return ['Hello world!\n']

def run_cherrypy_server(app, ip, port=8080):
  from cherrypy import wsgiserver
  server = wsgiserver.CherryPyWSGIServer(
                      (ip, port), app, server_name='www.cherrypy.example')
  server.start()

class Root:
  def index( self ):
    return "Primer Intento"

if __name__ == '__main__':
  ip   = os.environ['OPENSHIFT_PYTHON_IP']
  port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
  app = TransLogger( application )
  conf = { '/': {'tools.wsgiapp.on': True,
            'tools.wsgiapp.app': app,
            'tools.gzipon': True}}
  run_cherrypy_server( app, ip, port )


