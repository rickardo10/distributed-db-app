import cherrypy
from cherrypy import wsgiserver
import os

def application( environ, start_response ):
	status = '200 OK'
	body = """
	<html>
		<body>
			<a href = "/set">Test 1</a>
		</body>
	</html>
	"""
	response_headers = [ ('Content-type', 'text/html')]
	start_response( status, response_headers )
	return [body]

def set( self ):
	return ["prueba superada"]

d = wsgiserver.WSGIPathInfoDispatcher({'/': my_crazy_app, '/set': set})

if __name__ == '__main__':
	ip   = os.environ['OPENSHIFT_PYTHON_IP']
	port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
	server = wsgiserver.CherryPyWSGIServer( ( ip, port ), 
		d, server_name = 'www.cherrypy.example')
	server_namer.start()