#!/usr/bin/env python

import cherrypy
import database as db
import datetime

_header = """
<html>
<head>
<title>Investigador</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" media="all" href="niceforms-default.css" />
</head>
<body><div id="container">
"""

_footer = """
<p id="footer"><br />&copy;Ricardo Ocampo<br />Last update: 10 Septiembre 2013</p>
</div></body>
</html>
"""

_index = """
<ul>
	<li>
		<a href = "/investigador">Investigador</a>
	</li>
	<li>
		<a href = "/asistente">Asistente</a>
	</li>
	<li>
		<a href = "/asignarTarea">Asignar tarea</a>
	</li>
	<li>
		<a href = "/workingPaper">Working Paper</a>
	</li>
		<li>
		<a href = "/asiglist">Lista de Asignaciones</a>
	</li>
</ul>
"""

_investigador = """
<form action="saveAuthor" method="post" class="niceform">
	<fieldset>
    	<legend>Investigador</legend>
        <dl>
        	<dt><label for="nombre">Nombre:</label></dt>
            <dd><input type="text" name="nombre" id="nombre" size="32" maxlength="128" /></dd>
        </dl>
        <dl>
        	<dt><label for="email">E-mail:</label></dt>
            <dd><input type="text" name="email" id="email" size="32" maxlength="32" /></dd>
        </dl>
        <dl>
        	<input type="submit" value="Guardar">
        </dl>
    </fieldset>
</form>
"""

_asistente = """
<form action="saveAsistente" method="post" class="niceform">
	<fieldset>
    	<legend>Asistente</legend>
        <dl>
        	<dt><label for="nombre">Nombre:</label></dt>
            <dd><input type="text" name="nombre" id="nombre" size="32" maxlength="128" /></dd>
        </dl>
        <dl>
        	<dt><label for="email">E-mail:</label></dt>
            <dd><input type="text" name="email" id="email" size="32" maxlength="32" /></dd>
        </dl>
        <dl>
        	<dt><label for="telefono">Telefono:</label></dt>
            <dd><input type="text" name="telefono" id="telefono" size="32" maxlength="32" /></dd>
        </dl>
        <dl>
        	<input type="submit" value="Guardar">
        </dl>
    </fieldset>
</form>
"""

_asignar1 = """
<form action="asignarTarea2" method="post" class="niceform">
	<fieldset>
    	<legend>Asignación de tarea</legend>
        <dl>
        	<dt><label for="asignador">Asignado por:</label></dt>
        		<dd><select name = "investigador" >
        			<option selected>---Investigador---</option>
        			%s
        		</dd></select>
        </dl>
        <dl>
        <dl>
        	<input type="submit" value="Siguiente">
        </dl>
    </fieldset>
</form>
"""

_asignar = """
<form action="tareaAsignada" method="post" class="niceform">
	<fieldset>
    	<legend>Asignación de tarea</legend>
        <dl>
        	<dt><label for="asignador">Proyecto:</label></dt>
        		<dd><select name = "workingpaper" >
        			<option selected>---Working Paper---</option>
        			%s
        		</dd></select>
        </dl>
        <dl>
        	<dt><label for="asignacion">Asignar a:</label></dt> 
        		%s
        </dl>
        <dl>
        	<dt><label for="descripcion">Descripción de la Asignación:</label></dt>
            <dd><input type="text" name="descripcion" id="descripcion" size="32" maxlength="200" /></dd>
        </dl>
        <dl>
        	<dt><label for="prioridad">Prioridad:</label></dt>
            <dd><input type="radio" name = "prioridad" value = "1"> Alta</dd>
        		<dd><input type="radio" name = "prioridad" value = "2"> Media</dd>
       		<dd><input type="radio" name = "prioridad" value = "2"> Baja</dd>
        </dl>
        <dl>
        	<input type="submit" value="Guardar">
        </dl>
    </fieldset>
</form>
"""

_wp = """
<form action="saveWorkingPaper" method="post" class="niceform">
	<fieldset>
    	<legend>Working Papers</legend>
        <dl>
        	<dt><label for="workingpaper">Nombre del proyecto:</label></dt>
            <dd><input type="text" name="nombre" id="nombre" size="32" maxlength="128" /></dd>
        </dl>
        <dl>
        	<dt><label for="autor">Autor del proyecto:</label></dt>
            %s
        </dl>
        <dl>
        	<input type="submit" value="Guardar">
        </dl>
    </fieldset>
</form>
"""

class HelloWorld(object):
	# Main page
	def index( self ):
		return [ _header, _index, _footer ]
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
	def asignarTarea( self ):
		database = db.database( "basedatosCAP.db" )
		investigadores = database.getNames( "investigador" )
		_inv = ""
		
		# Creates a list with all reasearchers
		for x in investigadores:
			_inv = _inv + """<option value = %d>%s</option>""" % ( database.getId( "investigador", x), x ) 

		return [ _header, _asignar1 % (_inv ), _footer ]
	asignarTarea.exposed = True

	# Tasking 2
	def asignarTarea2( self, investigador ):
		database = db.database( "basedatosCAP.db" )
		asistentes = database.getNames( "asistente" )
		proyectos = database.getWorkingPapers( int( investigador ) )
		_asist = ""
		_proy = ""
		
		# Creates a list with all the assistants
		for x in asistentes:
			_asist = _asist + """<dd><input type="radio" name = "asistente" value = "%d"> %s</dd>""" % ( database.getId( "asistente", x), x ) 
		
		# Creates a list with all reasearchers
		for x in proyectos:
			_proy = _proy + """<option value = %d>%s</option>""" % ( database.getIdWP(x), x ) 

		return [ _header, _asignar % (_proy, _asist), _footer ]
	asignarTarea2.exposed = True

	# Working papers page
	def workingPaper( self ):
		database = db.database( "basedatosCAP.db" )
		investigadores = database.getNames( "investigador" )
		_inv = ""
		for x in investigadores:
			_inv = _inv + """<dd><input type="radio" name = "investigador" value = "%d"> %s</dd>""" % ( database.getId( "investigador", x), x ) 
		
		return [_header, _wp % _inv, _footer ]
	workingPaper.exposed = True

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

		# Inserts a row with the new assistant
		query = "insert into asistente(nombre, email, telefono) values ( '%s', '%s', '%s' )" % ( nombre, email, telefono )
		results = database.insertData( query )
		return [ _header, _salvado, _footer ]
	saveAsistente.exposed = True

	# Page that pops when a task is succesfully assinged
	def tareaAsignada( self, workingpaper, asistente, prioridad, descripcion ):
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
		_header = """
		<html>
		<head>
		<title>Lista de tareas</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<link rel="stylesheet" type="text/css" media="all" href="niceforms-default.css" />
		</head>
		"""

		_body = """
		<body>
			<h1>Lista de Asignaciones</h1>
			<table border = "1" width = "1100" >
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
			%s
			</table>
		"""

		_row = """
		<td>%s</td> 
		"""

		_rowEven = """
		<tr class = "even" >%s</tr>
		"""
		database = db.database( "basedatosCAP.db" )


		asignaciones1 = database.getAsignments( 1 )
		asignaciones2 = database.getAsignments( 2 )
		asignaciones3 = database.getAsignments( 3 )
		asignaciones4 = database.getAsignments( 4 )
		asignaciones = asignaciones1 + asignaciones2 + asignaciones3 + asignaciones4

		rows = ""
		for x in asignaciones:
			data = database.getDataFromAsigId( x )[ 0 ]
			rows = rows + "<tr>" + (_row % ( database.getAuthorFromAsigId( x ) ) + _row % ( database.getWPFromAsigId(x) ) + _row % ( database.getAsFromAsigId(x) ) + _row % ( data[0] ) + _row % ( data[1] ) + _row % ( data[2] ) + _row % ( data[3] ) + _row % ( data[4] ) + _row % ( data[5] ) + _row % ( data[6] ) )+ _row % ( '<form action = "/deleteRow/%d"><button>Borrar</button></form>' ) % ( x ) + "</tr>"

		return [_header, _body % (rows), "<div><a href = '/'>Regresar</a></div> " ,_footer ]
	asiglist.exposed = True

	def deleteRow( self, row ):
		database = db.database("basedatosCAP.db")
		database.deleteRow( int(row) )
		raise cherrypy.HTTPRedirect("/asiglist")
	deleteRow.exposed = True

# Starts the webpage
if __name__ == '__main__':
	ip   = os.environ['OPENSHIFT_PYTHON_IP']
	port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
	
	http_conf = {'global': {'server.socket_port': port,
									'server.socket_host': ip}}
	cherrypy.config.update(http_conf)
	cherrypy.quickstart( HelloWorld() )

#=========================================================================================

