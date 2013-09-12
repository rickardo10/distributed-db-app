import cherrypy
from cherrypy import wsgiserver
import os

class Root():
	def application( environ, start_response ):
		status = '200 OK'
		response_headers = [ ('Content-type', 'text/plain')]
		start_response( status, response_headers )
		return ['Hello world!\n']


if __name__ == '__main__':
	port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
	ip   = os.environ['OPENSHIFT_PYTHON_IP']
	root = Root()
	server = wsgiserver.CherryPyWSGIServer( ( ip, port ), 
		root.application, server_name = 'www.cherrypy.example')
	server.start()