#!/usr/bin/env python

import cherrypy
import database as db
import datetime
import os
from pytz import timezone
from auth import AuthController, require, member_of, name_is
from restricted import RestrictedArea
import smtplib

_header = open("static/header.html").read()
_investigador = open("static/investigador.html").read()
_asistente = open("static/asistente.html").read()
_asignar = open("static/asignar.html").read()
_wp = open("static/wp.html").read()
_footer = open("static/footer.html").read() 
	
class HelloWorld(object):

	_cp_config={
		'tools.sessions.on': True,
		'tools.auth.on': True
	}

	# Forces to log in first
	auth = AuthController()

	# Creates a page that is only for administrator
	restricted = RestrictedArea()
	
	# Main page
	@require()
	def index( self ):
		return [ _header % ("Menú principal"), _footer ]
	index.exposed = True

	# Tasking
	@require()
	def asignartarea( self, investigador = "0" ):
		database = db.database( "basedatosCAP.db" )
		investigadores = database.getNames( "investigador" )
		asistentes = database.getNames( "asistente" )
		proyectos = database.getWorkingPapers( int(investigador) )

		_asist = ""
		_proy = ""
		_inv = "<option selected value="">-Investigador-</selected>"
		
		# Creates a list with all reasearchers
		if investigador != "0":
			_inv = "<option value = %d>%s</option>\n" % ( int(investigador), database.getName( "investigador", int(investigador) ) )

		for x in investigadores:
			if database.getId("investigador", x) != int(investigador):
				_inv = _inv + """<option value = %d>%s</option>\n""" % ( database.getId( "investigador", x), x ) 

		# Creates a list with all the assistants
		for x in asistentes:
			_asist = _asist + """<option value = "%d"> %s</option>\n""" % ( database.getId( "asistente", x), x ) 
		
		# Creates a list with all reasearchers
		for x in proyectos:
			_proy = _proy + """<option value = %d>%s</option>\n""" % ( database.getIdWP(x), x ) 	

		return [ _header % ("Asignar tarea"), _asignar % (_inv, _proy, _asist ), _footer ]
	asignartarea.exposed = True

	# Working papers page
	@require()
	def workingpaper( self ):
		database = db.database( "basedatosCAP.db" )
		investigadores = database.getNames( "investigador" )
		_inv = ""
		for x in investigadores:
			_inv = _inv + """<option value = "%d"> %s</option>""" % ( database.getId( "investigador", x), x ) 
		
		return [_header % ("Crear nuevo working paper"), _wp % _inv, _footer ]
	workingpaper.exposed = True

	# Page that pops when a task is succesfully assinged
	@require()
	def tareasignada( self, workingpaper, asistente, prioridad, descripcion, investigador, justificacion ):
		_salvado = """
			<p>Tarea correctamente asignada<p>
			<p> <a href = "/">Regresar</a>
		"""
		# Initializes an object of the database
		database = db.database( "basedatosCAP.db" )
		time = datetime.datetime.now(timezone('Mexico/General')).strftime("%b %d, %Y %H:%M %p")

		# Inserts a row with the new task
		query = "insert into asignaciones(descripcion, prioridad, fechaini ) values ( '%s', '%s', '%s' )" % ( descripcion, '3', time )
		results = database.insertData( query )
		query1 = "insert into linkasignaciones(asid, asigid, wpid ) values ( %d, %d, %d )" % ( int( asistente ), database.getIdAsig( descripcion ) , int( workingpaper ) )
		results1 = database.insertData( query1 )
		
		msg = 

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login("r.ocampo.vega@gmail.com", "Raov892009")


		return [ _header % (""), _salvado, _footer ]
	tareasignada.exposed = True


	# Page that pops when a working paper is succesfully created
	@require()
	def guardarwp( self, nombre, investigador ):
		_salvado = """
			<p>Working paper correctamente creado<p>
			<p> <a href = "/">Regresar</a>
		"""
		# Initializes an object of the database
		database = db.database( "basedatosCAP.db" )

		# Inserts a row with the new assistant
		query = "insert into workingpaper( nombrewp ) values ( '%s' )" % ( nombre )
		results = database.insertData( query )
		query1 = "insert into linkworkingpaper( invid, wpid ) values ( %d, %d )" % ( int( investigador ), database.getIdWP( nombre ))
		results1 = database.insertData( query1 )
		return [ _header % (""), _salvado, _footer ]
	guardarwp.exposed = True

# Starts the webpage
if __name__ == '__main__':
	ip   = os.environ['OPENSHIFT_PYTHON_IP']
	port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
	#port = 8000
	#ip = "127.0.0.1"

	http_conf = {'global': {'server.socket_port': port,
									'server.socket_host': ip}}
	cherrypy.config.update(http_conf)

	current_dir = os.path.dirname( os.path.abspath(__file__) )
	conf = {'/css':{'tools.staticdir.on':True, 
			  			 'tools.staticdir.dir': os.path.join(current_dir, 'css')},
			  '/js':{'tools.staticdir.on':True,
			  			'tools.staticdir.dir': os.path.join(current_dir, 'js')},
			  '/static':{'tools.staticdir.on':True,
			  				 'tools.staticdir.dir': os.path.join(current_dir, 'static')}}

	cherrypy.quickstart( HelloWorld(), "/", config = conf )

#=========================================================================================

