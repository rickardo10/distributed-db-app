from cherrypy import wsgiserver

def my_crazy_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type','text/plain')]
    start_response(status, response_headers)
    return ['Hello world!']

ip   = os.environ['OPENSHIFT_PYTHON_IP']
port = int(os.environ['OPENSHIFT_PYTHON_PORT'])				

server = wsgiserver.CherryPyWSGIServer(
            ( ip , port ), my_crazy_app,
            server_name='www.cherrypy.example')
server.start()