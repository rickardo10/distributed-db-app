#!/usr/bin/env python

import cherrypy
import database as db
import datetime
import os
from pytz import timezone
from auth import AuthController, require, member_of, name_is

_header_Admin = open("static/header_admin.html").read()
_investigador = open("static/investigador.html").read()
_asistente = open("static/asistente.html").read()
_asignar = open("static/asignar.html").read()
_wp = open("static/wp.html").read()
_footer = open("static/footer.html").read()
_style = open("css/style.css").read()
_script = open("js/some.js").read()
name = ""

class RestrictedArea:
	# all methods in this controller (and subcontrollers) is
   # open only to members of the admin group
	_cp_config = {
		'auth.require': [member_of("admin")]
	}

	def index(self):
		globals()["name"] = "Menú principal administrador"
		return [ _header_Admin % globals(), _footer]
	index.exposed = True

   # Researchers page
	def investigador( self ):
		globals()["name"] = "Añadir investigador"
		return [ _header_Admin % globals(), _investigador, _footer ]
	investigador.exposed = True

	# Research assistants page
	def asistente( self ):
		globals()["name"] = "Añadir asistente"
		return [ _header_Admin % globals(), _asistente, _footer ]
	asistente.exposed = True

	# Page that pops when a researcher is succesfully saved
	def guardarinvestigador( self, nombre, email ):
		_salvado = """
			<p>Investigador correctamente salvado<p>
			<p> <a href = "/">Regresar</a>
		"""
		database = db.database( "basedatosCAP.db" )
		query = "insert into investigador(nombre, email) values ( '%s', '%s' )" % ( nombre, email )
		results = database.insertData( query )
		return [ _header_Admin % (""), _salvado, _footer ]
	guardarinvestigador.exposed = True

	# Page that pops when a research assistant is succesfully saved
	def guardarasistente( self, nombre, email, telefono ):
		_salvado = """
			<p>Asistente correctamente salvado<p>
			<p> <a href = "/">Regresar</a>
		"""
		# Initializes an object of the database
		database = db.database( "basedatosCAP.db" )
		asistentes = database.getNames("asistente")
		if nombre in asistentes:
			return [_header_Admin % globals(), _asistente, "El asistente ya existe" , _footer] 

		# Inserts a row with the new assistant
		query = "insert into asistente(nombre, email, telefono) values ( '%s', '%s', '%s' )" % ( nombre, email, telefono )
		results = database.insertData( query )
		return [ _header_Admin % globals(), _salvado, _footer ]
	guardarasistente.exposed = True

	# Displays the list of assignments
	def asiglist( self, row = 0 ):

		_table = open("static/table.html").read()
		row = int( row )
		_row = '<td>%s</td>' 

		database = db.database( "basedatosCAP.db" )

		asignaciones1 = database.getAsignments( 1 )
		asignaciones2 = database.getAsignments( 2 )
		asignaciones3 = database.getAsignments( 3 )
		asignaciones4 = database.getAsignments( 4 )
		asignaciones = asignaciones1 + asignaciones2 + asignaciones3 + asignaciones4

		rows = ""
		if row != 0: data = database.getDataFromAsigId( row )
		_prioridad = """
				<select id="prioridad" name = "prioridad">
		         <option %s value = "1">Alta</option>
		        	<option %s value = "2">Media</option>
		       	<option %s value = "3">Baja</option>
	       	</select>
	   """
		prioridades = [ "1", "2", "3"] 

		_avance = """
				<select id="avance" name = "avance">
		         <option %s value = "10%%">10%%</option>
		        	<option %s value = "20%%">20%%</option>
		       	<option %s value = "30%%">30%%</option>
		       	<option %s value = "40%%">40%%</option>
		        	<option %s value = "50%%">50%%</option>
		       	<option %s value = "60%%">60%%</option>
		       	<option %s value = "70%%">70%%</option>
		        	<option %s value = "80%%">80%%</option>
		       	<option %s value = "90%%">90%%</option>
	       	</select>
	   """
		avances = ["10%%", "20%%", "30%%", "40%%", "50%%", "60%%", "70%%", "80%%", "90%%"]

		_estado = """
				<select id = "estado" name = "estado" >
					<option %s value = "En proceso">En proceso</option>
					<option %s value = "Pausado">Pausado</option>
					<option %s value = "Terminado">Terminado</option>
				</select>
		"""
		estados = ["En proceso", "Pausado", "Terminado"]

		_asignado = """
				<select id = "asignado" name = "asistente" >
	        	%s
	        	</select>
	   """

		_asist = ""
		asistentes = database.getNames( "asistente" )
	   # Creates a list with all the assistants
		if row != 0:
			for x in asistentes:
				if x == database.getAsFromAsigId( row ):
					s = 'selected'
				else:
					s = ''
				_asist = _asist + """<option %s value = "%d"> %s</option>\n""" % ( s, database.getId( "asistente", x), x ) 


			_lineToEdit = "<tr>" + (_row % ( database.getAuthorFromAsigId( row ) ) + 
												  _row % ( database.getWPFromAsigId( row ) ) + 
												  _row % ( _asignado % _asist  ) + 
												  _row % ( data[0] ) + 
												  _row % ( _estado % tuple([ "selected" if x == data[1] else "" for x in estados])) + 
												  _row % ( _prioridad % tuple([ "selected" if x == data[2] else "" for x in prioridades])) + 
												  _row % ( _avance % tuple([ "selected" if x == data[3] else "" for x in avances]) ) + 
												  _row % ( data[4] ) + 
												  _row % ( data[5] ) +  
												  _row % ( "<textarea id='comment'>" + str(data[6]) +"</textarea>" ) + 
												  _row % (( """<p><button onclick='guardar(%d)' class='btn btn-primary btn-mini'>Guardar</button></p>""" ) % ( row )  +
																"""<button onclick='terminado(%d)' class='btn btn-primary btn-mini'>Terminado</button>""" % ( row ) ) +
											"</tr>" )

		for x in asignaciones:
			if x != row:			
				data = database.getDataFromAsigId( x )
				rows = rows + "<tr>" + ( _row % ( database.getAuthorFromAsigId( x ) ) +
										_row % ( database.getWPFromAsigId( x ) ) +
										_row % ( database.getAsFromAsigId( x ) ) +
										'\n'.join( [ _row % ( y ) for y in data ] ) +
										_row % ( """<p><button onclick='editrow(%d)' class='btn btn-primary btn-mini'>Editar</button></p>""" % x +
											  "</tr>"))
			else:
				rows = rows + _lineToEdit

		_table = _table % ("Lista de asignaciones", rows )
		return [_table, "<div><a href = '/restricted'>Regresar</a></div> " ,_footer ]
	asiglist.exposed = True

	def updaterow( self, row, asignado, estado, prioridad, avance, comentarios ):
		database = db.database("basedatosCAP.db")
		database.updateRow( int(row), int(asignado), estado, prioridad, avance, comentarios )
		raise cherrypy.HTTPRedirect("/restricted/asiglist")
	updaterow.exposed = True

	def terminado( self, row ):
		database = db.database("basedatosCAP.db")
		time = datetime.datetime.now(timezone('Mexico/General')).strftime("%b %d, %Y %H:%M %p")
		database.insertData("update asignaciones set fechafin = '%s' where rowid = %d" % (time, int(row) ) )
		raise cherrypy.HTTPRedirect("/restricted/asiglist")
	terminado.exposed = True

		# Tasking
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

		globals()["name"] = "Asignar tarea"
		return [ _header_Admin % globals(), _asignar % (_inv, _proy, _asist ), _footer ]
	asignartarea.exposed = True

	# Working papers page
	def workingpaper( self ):
		database = db.database( "basedatosCAP.db" )
		investigadores = database.getNames( "investigador" )
		_inv = ""
		for x in investigadores:
			_inv = _inv + """<option value = "%d"> %s</option>""" % ( database.getId( "investigador", x), x ) 
		
		globals()["name"] = "Crear nuevo working paper"
		return [_header_Admin % globals(), _wp % _inv, _footer ]
	workingpaper.exposed = True

	# Page that pops when a task is succesfully assinged
	def tareasignada( self, workingpaper, asistente, prioridad, descripcion, investigador ):
		_salvado = """
			<p>Tarea correctamente asignada<p>
			<p> <a href = "/">Regresar</a>
		"""
		# Initializes an object of the database
		database = db.database( "basedatosCAP.db" )
		time = datetime.datetime.now(timezone('Mexico/General')).strftime("%b %d, %Y %H:%M %p")

		# Inserts a row with the new task
		query = "insert into asignaciones(descripcion, prioridad, fechaini ) values ( '%s', '%s', '%s' )" % ( descripcion, prioridad, time )
		results = database.insertData( query )
		query1 = "insert into linkasignaciones(asid, asigid, wpid ) values ( %d, %d, %d )" % ( int( asistente ), database.getIdAsig( descripcion ) , int( workingpaper ) )
		results1 = database.insertData( query1 )
		return [ _header_Admin % globals(), _salvado, _footer ]
	tareasignada.exposed = True


	# Page that pops when a working paper is succesfully created
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
		return [ _header_Admin % globals(), _salvado, _footer ]
	guardarwp.exposed = True