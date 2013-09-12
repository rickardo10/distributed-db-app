import cherrypy

class Root(object):
	def index(self):
		return "Hello World"
	main.expose = True

if __name__ == '__main__':
	http_conf = {'global': {'server.socket_port': port,
									'server.socket_host': ip}}
	cherrypy.config.update(http_conf)
	cherrypy.engine.start()