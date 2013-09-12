import cherrypy
import os

def application( environ, start_response ):
	status = '200 OK'
	response_headers = [ ('Content-type', 'text/plain')]
	start_response( status, response_headers )
	return ['Hello world!\n']


class Root:
	def index( self ):
		return "Primer Intento"

if __name__ == '__main__':
	port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
	ip   = os.environ['OPENSHIFT_PYTHON_IP']

	conf = {'server.socket_host': ip, 'server.socket_port': port}
	cherrypy.config.update(conf)
	conf = { '/': { 'tools.wsgiapp.on': True,
						 'tools.wsgiapp.app': application,
						 'tools.gzip.on': True}}
	cherrypy.tree.mount(Root(), '/', config = conf )
	cherrypy.engine.start()