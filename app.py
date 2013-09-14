#!/usr/bin/env python

import cherrypy
import database as db
import datetime
import os

_header = """
<html>
<head>
<title>Investigador</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" media="all" href="style.css" />
<script type="application/javascript" src="some.js"></script>
</head>
<body>
	<div>
		<a href="/" class="pure-menu-heading">Menu</a>
		<ul>
			<li><a href = "/investigador">Investigador</a></li>
			<li><a href = "/asistente">Asistente</a></li>
			<li><a href = "/asignartarea">Asignar tarea</a></li>
			<li><a href = "/workingpaper">Working Paper</a></li>
			<li><a href = "/asiglist">Lista de Asignaciones</a></li>
		</ul>
	</div>
	<div id = "signup-form">
		<div id = "signup-form-inner">
			<div class="clearfix" id="header">
				<h1>Investigador</h1>
			</div>
			<p>Por favor complete cada uno de los campos, asegurandose de
			utilizar un email correcto ya que se le enviará un código de 
			validación.</p>
"""

_investigador = """
			<form id="send" action="saveAuthor" method="post">
				<p>
					<label for="nombre">Nombre:</label>
					<input type="text" name="nombre" id="nombre" maxlength="128" placeholder="Nombre"/>
				</p>
				<p>
					<label for="email">E-mail:</label>
					<input type="text" name="email" id="email" maxlength="32" placeholder="E-mail"/>
				</p>
				<p>
					<button class="btn btn-primary" type="submit">Guardar</button>
				</p>
			</form>
"""

_asistente = """
			<form id="send" action="saveAsistente" method="post">
				<p>
					<label for="nombre">Nombre:</label>
					<input type="text" name="nombre" id="nombre" maxlength="128" placeholder="Nombre"/>
				</p>
				<p>
					<label for="email">E-mail:</label>
					<input type="text" name="email" id="email" maxlength="32" placeholder="E-mail"/>
				</p>
				<p>
					<label for="telefono">Teléfono:</label>
					<input type="text" name="telefono" id="telefono" maxlength="32" placeholder="Teléfono"/>
				</p>
				<p>
					<button class="btn btn-primary" type="submit">Guardar</button>
				</p>
			</form>
"""

_asignar = """
			<form id="asignacion" action="tareaAsignada" method="post" class="pure-form" >
				<p>
					<label for="asignador">Asignado por:</label>
					<select name = "investigador" id = "invest" onchange="onChangeSetVar()">
					%s
					</select>
				</p>
			<p>
	        	<label for="asignador">Proyecto:</label>
	        	<select name = "workingpaper" >
		        	<option selected>-Working Paper-</option>
		        	%s
	        	</select>
         </p>
         <p>
	         <label for="asignacion">Asignar a:</label>
	         <select name = "asistente" >
	        	%s
	        	</select>
        	</p>
        	<p>
	        	<label for="descripcion">Descripción de la Asignación:</label></dt>
	         <input type="text" name="descripcion" id="descripcion" maxlength="200"/>
        	</p>
        	<p>
	        	<label for="prioridad">Prioridad:</label>
	        	<select name = "prioridad">
		         <option value = "1">Alta</option>
		        	<option value = "2">Media</option>
		       	<option value = "3">Baja</option>
	       	</select>
        	</p>
        	<p>
        		<button class="btn btn-primary" type="submit">Guardar</button>
			</p>
			</form>
"""

_wp = """
			<form action="saveWorkingPaper" method="post">
				<p>
					<label for="workingpaper">Nombre del proyecto:</label>
					<input type="text" name="nombre" id="nombre" maxlength="128"/>
				</p>
				<p>
					<label for="autor">Autor del proyecto:</label>
					<select name = "investigador">
					%s
					</select>
				</p>
				<p>
					<button class="btn btn-primary" type="submit">Guardar</button> 
				<p>
				</form>
"""

_footer = """
		<div id="required">
			<p>&copy;Autor: Ricardo Ocampo<br/>
			Last update: 13 Septiembre 2013</p>
		</div>
	</div>
</body>
</html>
"""

class HelloWorld(object):
	# Main page
	def index( self ):
		return [ _header, _footer ]
	index.exposed = True

	# Researchers page
	def investigador( self ):
		return [ _header, _investigador, _footer ]
	investigador.exposed = True

	# Research assistants page
	def asistente( self ):
		return [ _header, _asistente, _footer ]
	asistente.exposed = True

	# Tasking
	def asignartarea( self, investigador = "0" ):
		database = db.database( "basedatosCAP.db" )
		investigadores = database.getNames( "investigador" )
		asistentes = database.getNames( "asistente" )
		proyectos = database.getWorkingPapers( int(investigador) )

		_asist = ""
		_proy = ""
		_inv = ""
		
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

		return [ _header, _asignar % (_inv, _proy, _asist ), _footer ]
	asignartarea.exposed = True

	# Working papers page
	def workingpaper( self ):
		database = db.database( "basedatosCAP.db" )
		investigadores = database.getNames( "investigador" )
		_inv = ""
		for x in investigadores:
			_inv = _inv + """<option value = "%d"> %s</option>""" % ( database.getId( "investigador", x), x ) 
		
		return [_header, _wp % _inv, _footer ]
	workingpaper.exposed = True

	# Page that pops when a researcher is succesfully saved
	def saveAuthor( self, nombre, email ):
		_salvado = """
			<p>Investigador correctamente salvado<p>
			<p> <a href = "/">Regresar</a>
		"""
		database = db.database( "basedatosCAP.db" )
		query = "insert into investigador(nombre, email) values ( '%s', '%s' )" % ( nombre, email )
		results = database.insertData( query )
		return [ _header, _salvado, _footer ]
	saveAuthor.exposed = True

	# Page that pops when a research assistant is succesfully saved
	def saveAsistente( self, nombre, email, telefono ):
		_salvado = """
			<p>Asistente correctamente salvado<p>
			<p> <a href = "/">Regresar</a>
		"""
		# Initializes an object of the database
		database = db.database( "basedatosCAP.db" )
		asistentes = database.getNames("asistente")
		if nombre in asistentes:
			return [_header, _asistente, "El asistente ya existe" , _footer] 

		# Inserts a row with the new assistant
		query = "insert into asistente(nombre, email, telefono) values ( '%s', '%s', '%s' )" % ( nombre, email, telefono )
		results = database.insertData( query )
		return [ _header, _salvado, _footer ]
	saveAsistente.exposed = True

	# Page that pops when a task is succesfully assinged
	def tareaAsignada( self, workingpaper, asistente, prioridad, descripcion, investigador ):
		_salvado = """
			<p>Tarea correctamente asignada<p>
			<p> <a href = "/">Regresar</a>
		"""
		# Initializes an object of the database
		database = db.database( "basedatosCAP.db" )
		time = datetime.datetime.now().strftime("%d-%m-%y")

		# Inserts a row with the new task
		query = "insert into asignaciones(descripcion, prioridad, fechaini ) values ( '%s', '%s', '%s' )" % ( descripcion, prioridad, time )
		results = database.insertData( query )
		query1 = "insert into linkasignaciones(asid, asigid, wpid ) values ( %d, %d, %d )" % ( int( asistente ), database.getIdAsig( descripcion ) , int( workingpaper ) )
		results1 = database.insertData( query1 )
		return [ _header, _salvado, _footer ]
	tareaAsignada.exposed = True


	# Page that pops when a working paper is succesfully created
	def saveWorkingPaper( self, nombre, investigador ):
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
		return [ _header, _salvado, _footer ]
	saveWorkingPaper.exposed = True

	# Displays the list of assignments
	def asiglist( self ):
		_body = """
		<body>
			<table class="table table-striped">
				<thead>
					<tr>
						<th>Autor</th>
						<th>Working Paper</th>
						<th>Asignado</th>
						<th>Descripción</th>
						<th>Estado</th>
						<th>Prioridad</th>
						<th>Avance</th>
						<th>Fecha de Inicio</th>
						<th>Fecha de Culminación</th>
						<th>Comentarios</th>
						<th>Editar</th>
					</tr>
				</thead>
				<tbody>
					%s
				</tbody>
			</table>
		"""

		_row = """
		<td>%s</td> 
		"""

		database = db.database( "basedatosCAP.db" )


		asignaciones1 = database.getAsignments( 1 )
		asignaciones2 = database.getAsignments( 2 )
		asignaciones3 = database.getAsignments( 3 )
		asignaciones4 = database.getAsignments( 4 )
		asignaciones = asignaciones1 + asignaciones2 + asignaciones3 + asignaciones4

		rows = ""
		counter = 1
		for x in asignaciones:
			data = database.getDataFromAsigId( x )[ 0 ]
			rows = rows + "<tr>" + (_row % ( database.getAuthorFromAsigId( x ) ) + _row % ( database.getWPFromAsigId(x) ) + _row % ( database.getAsFromAsigId(x) ) + _row % ( data[0] ) + _row % ( data[1] ) + _row % ( data[2] ) + _row % ( data[3] ) + _row % ( data[4] ) + _row % ( data[5] ) + _row % ( data[6] ) )+ _row % ( '<form action = "/deleteRow/%d"><button class="btn btn-primary">Borrar</button></form>' ) % ( x ) + "</tr>"

		return [_header, _body % (rows), "<div><a href = '/'>Regresar</a></div> " ,_footer ]
	asiglist.exposed = True

	def deleteRow( self, row ):
		database = db.database("basedatosCAP.db")
		database.deleteRow( int(row) )
		raise cherrypy.HTTPRedirect("/asiglist")
	deleteRow.exposed = True

# Starts the webpage
if __name__ == '__main__':
	current_dir = os.path.dirname( os.path.abspath(__file__) )
	#ip   = os.environ['OPENSHIFT_PYTHON_IP']
	#port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
	
	#http_conf = {'global': {'server.socket_port': port,
	#								'server.socket_host': ip}}
	#cherrypy.config.update(http_conf)

	conf = {'/style.css':{'tools.staticfile.on':True, 
			  					 'tools.staticfile.filename':current_dir+"/style.css"},
			  '/some.js':{'tools.staticfile.on':True,
			  				  'tools.staticfile.filename':current_dir+"/some.js"}}
	

	cherrypy.quickstart( HelloWorld(), "/", config = conf )

#=========================================================================================

