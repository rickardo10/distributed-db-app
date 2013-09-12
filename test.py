import cherrypy
from pasteself.translogger import Translogger

def application( environ, start_response ):
	status = '200 OK'
	response_headers = [('Content-type', 'text/plain')]
	start_response( status,  response_headers )
	return ['Hello world!\n']


class Root:
	def index( self ):
		return "Primer Intento"

if __name__ == '__main__':
	app = TransLogger( application )
	conf = { '/': {'tools.wsgiapp.on': True,
						'tools.wsgiapp.app': app,
						'tools.gzipon': True}}
	cherrypy.tree.mount(Root(), '/', config = conf )
	cherrypy.server.quickstart()
	cherrypy.engine.start()


