import cherrypy
from cherrypy import wsgiserver
import os

def application( environ, start_response ):
	status = '200 OK'
	response_headers = [ ('Content-type', 'text/plain')]
	start_response( status, response_headers )
	body = """
	<html>
		<body>
			<a href = "/set">Test 1</a>
		</body>
	</html>
	"""
	return [body]

def set( self ):
	return ["prueba superada"]
set.expose = True


if __name__ == '__main__':
	ip   = os.environ['OPENSHIFT_PYTHON_IP']
	port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
	server = wsgiserver.CherryPyWSGIServer( ( ip, port ), 
		application, server_name = 'www.cherrypy.example')
	server.start()