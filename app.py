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
			<li><a href = "/asignarTarea">Asignar tarea</a></li>
			<li><a href = "/workingPaper">Working Paper</a></li>
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
					<button id="submit" type="submit">Guardar</button>
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
					<button id="submit" type="submit">Guardar</button>
				</p>
			</form>
"""

_asignar1 = """
<form action="asignarTarea2" method="post" class="pure-form pure-form-stacked">
<label for="asignador">Asignado por:</label>
<select name = "investigador" onchange = "hola">
<option selected>-Investigador-</option>
%s
</select>
<input type="submit" value="Siguiente" class="pure-button pure-button-primary">
</form>
"""

_asignar = """
<form action="tareaAsignada" method="post" class="pure-form pure-form-stacked">
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
       		<dd><input type="radio" name = "prioridad" value = "3"> Baja</dd>
        </dl>
        <dl>
        	<input type="submit" value="Guardar" class="pure-button pure-button-primary">
        </dl>
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

_wp = """
<form action="saveWorkingPaper" method="post" class="pure-form pure-form-stacked">
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
        	<input type="submit" value="Guardar" class="pure-button pure-button-primary"> 
        </dl>
    </fieldset>
</form>
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
	def asignarTarea( self ):
		database = db.database( "basedatosCAP.db" )
		investigadores = database.getNames( "investigador" )
		_inv = ""
		
		# Creates a list with all reasearchers
		for x in investigadores:
			_inv = _inv + """<option value = %d>%s</option>\n""" % ( database.getId( "investigador", x), x ) 

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
			_asist = _asist + """<dd><input type="radio" name = "asistente" value = "%d"> %s</dd>\n""" % ( database.getId( "asistente", x), x ) 
		
		# Creates a list with all reasearchers
		for x in proyectos:
			_proy = _proy + """<option value = %d>%s</option>\n""" % ( database.getIdWP(x), x ) 

		_investigador = """
			<fieldset class = pure-form pure-form-stacked>
		    	<legend>Asignación de tarea</legend>
		        <dl>
		        	<dt><label for="asignador">Asignado por:</label></dt>
		        		<dd><select name = "investigador" >
		        			<option selected>%s</option>
		        		</dd></select>
		        </dl>
		        <dl>
			</form>
			"""
		database.getName("investigador", investigador)
		return [ _header, _investigador % (database.getName("investigador", investigador)) ,_asignar % (_proy, _asist), _footer ]
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
		asistentes = database.getNames("asistente")
		if nombre in asistentes:
			return [_header, _asistente, "El asistente ya existe" , _footer] 

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
		_body = """
		<body>
			<h1>Lista de Asignaciones</h1>
			<table class="pure-table">
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
			if counter % 2 == 0:
				rows = rows + "<tr class = 'pure-table-odd'>" + (_row % ( database.getAuthorFromAsigId( x ) ) + _row % ( database.getWPFromAsigId(x) ) + _row % ( database.getAsFromAsigId(x) ) + _row % ( data[0] ) + _row % ( data[1] ) + _row % ( data[2] ) + _row % ( data[3] ) + _row % ( data[4] ) + _row % ( data[5] ) + _row % ( data[6] ) )+ _row % ( '<form action = "/deleteRow/%d"><button>Borrar</button></form>' ) % ( x ) + "</tr>"
			else:
				rows = rows + "<tr>" + (_row % ( database.getAuthorFromAsigId( x ) ) + _row % ( database.getWPFromAsigId(x) ) + _row % ( database.getAsFromAsigId(x) ) + _row % ( data[0] ) + _row % ( data[1] ) + _row % ( data[2] ) + _row % ( data[3] ) + _row % ( data[4] ) + _row % ( data[5] ) + _row % ( data[6] ) )+ _row % ( '<form action = "/deleteRow/%d"><button>Borrar</button></form>' ) % ( x ) + "</tr>"
			counter += 1

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
			  					 'tools.staticfile.filename':current_dir+"/style.css"
			  					}}
	

	cherrypy.quickstart( HelloWorld(), "/", config = conf )

#=========================================================================================

