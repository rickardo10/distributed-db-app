import cherrypy
import os

class Root(object):
	def index(self):
		return "Hello World"
	index.expose = True

if __name__ == '__main__':
	ip   = os.environ['OPENSHIFT_PYTHON_IP']
	port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
	
	http_conf = {'global': {'server.socket_port': port,
									'server.socket_host': ip}}
	cherrypy.config.update(http_conf)
	cherrypy.tree.mount(Root(), '/')
	cherrypy.engine.start()