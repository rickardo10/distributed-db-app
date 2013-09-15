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
	<div class="pure-menu pure-menu-open">
		<a href="/" class="pure-menu-heading">Menu</a>
		<ul>
			<li><a href = "/investigador">Añadir investigador</a></li>
			<li><a href = "/asistente">Añadir asistente</a></li>
			<li><a href = "/workingpaper">Crear nuevo working paper</a></li>
			<li><a href = "/asignartarea">Asignar nueva tarea</a></li>
			<li class="pure-menu-heading">Tablas</li>
			<li><a href = "/asiglist">Lista de asignaciones</a></li>
		</ul>
	</div>
	<div id = "signup-form">
		<div id = "signup-form-inner">
			<div class="clearfix" id="header">
				<h1>%s</h1>
			</div>
"""

_investigador = """
			<form id="send" action="guardarinvestigador" method="post">
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
			<form id="send" action="guardarinvestigador" method="post">
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
			<form id="asignacion" action="tareasignada" method="post" class="pure-form" >
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
	         <input type="text" name="descripcion" maxlength="200"/>
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
			<form action="guardarwp" method="post">
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
			Last update: 14 Septiembre 2013</p>
		</div>
	</div>
</body>
</html>
"""

class HelloWorld(object):
	# Main page
	def index( self ):
		return [ _header % ("Menú principal"), _footer ]
	index.exposed = True

	# Researchers page
	def investigador( self ):
		return [ _header % ("Añadir investigador"), _investigador, _footer ]
	investigador.exposed = True

	# Research assistants page
	def asistente( self ):
		return [ _header % ("Añadir asistente"), _asistente, _footer ]
	asistente.exposed = True

	# Tasking
	def asignartarea( self, investigador = "0" ):
		database = db.database( "basedatosCAP.db" )
		investigadores = database.getNames( "investigador" )
		asistentes = database.getNames( "asistente" )
		proyectos = database.getWorkingPapers( int(investigador) )

		_asist = ""
		_proy = ""
		_inv = "<option selected>-Investigador-</selected>"
		
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
	def workingpaper( self ):
		database = db.database( "basedatosCAP.db" )
		investigadores = database.getNames( "investigador" )
		_inv = ""
		for x in investigadores:
			_inv = _inv + """<option value = "%d"> %s</option>""" % ( database.getId( "investigador", x), x ) 
		
		return [_header % ("Crear nuevo working paper"), _wp % _inv, _footer ]
	workingpaper.exposed = True

	# Page that pops when a researcher is succesfully saved
	def guardarinvestigador( self, nombre, email ):
		_salvado = """
			<p>Investigador correctamente salvado<p>
			<p> <a href = "/">Regresar</a>
		"""
		database = db.database( "basedatosCAP.db" )
		query = "insert into investigador(nombre, email) values ( '%s', '%s' )" % ( nombre, email )
		results = database.insertData( query )
		return [ _header % (""), _salvado, _footer ]
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
			return [_header % (""), _asistente, "El asistente ya existe" , _footer] 

		# Inserts a row with the new assistant
		query = "insert into asistente(nombre, email, telefono) values ( '%s', '%s', '%s' )" % ( nombre, email, telefono )
		results = database.insertData( query )
		return [ _header % (""), _salvado, _footer ]
	guardarinvestigador.exposed = True

	# Page that pops when a task is succesfully assinged
	def tareasignada( self, workingpaper, asistente, prioridad, descripcion, investigador ):
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
		return [ _header % (""), _salvado, _footer ]
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
		return [ _header % (""), _salvado, _footer ]
	guardarwp.exposed = True

	# Displays the list of assignments
	def asiglist( self, row = 0 ):
		row = int( row )
		_header = """
		<html>
		<head>
		<title>Investigador</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<link rel="stylesheet" type="text/css" media="all" href="style.css" />
		<script type="application/javascript" src="some.js"></script>
		</head>
		<body>
			<div id = "signup-form-inner">
				<div class="clearfix" id="header">
					<h1>%s</h1>
				</div>
		"""
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
		if row != 0: data = database.getDataFromAsigId( row )
		_prioridad = """
				<select id="asignado" name = "prioridad">
		         <option %s value = "1">Alta</option>
		        	<option %s value = "2">Media</option>
		       	<option %s value = "3">Baja</option>
	       	</select>
	   """

		_avance = """
				<select id="asignado" name = "avance">
		         <option %s value = "10">10%%</option>
		        	<option %s value = "20">20%%</option>
		       	<option %s value = "30">30%%</option>
		       	<option %s value = "40">40%%</option>
		        	<option %s value = "50">50%%</option>
		       	<option %s value = "60">60%%</option>
		       	<option %s value = "70">70%%</option>
		        	<option %s value = "80">80%%</option>
		       	<option %s value = "90">90%%</option>
	       	</select>
	   """
		prioridades = ["10", "20", "30", "40", "50", "60", "70", "80", "90"]

		_estado = """
				<select id = "asignado" name = "estado" >
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
												  _row % ( _estado % tuple([ "selected" if x is data[1] else "" for x in estados])) + 
												  _row % ( _prioridad % tuple([ "selected" if x + 1 is data[2] else "" for x in range(3)])) + 
												  _row % ( _avance % tuple([ "selected" if x is data[3] else "" for x in prioridades]) ) + 
												  _row % ( data[4] ) + 
												  _row % ( data[5] ) +  
												  _row % ( "<textarea id='comment'>" + str(data[6]) +"</textarea>" ) + 
												  _row % (( """<p><button onclick='guardar(%d)' class='btn btn-primary btn-mini'>Guardar</button></p>""" ) % ( row ) )  +
											"</tr>" )

		for x in asignaciones:
			if x != row:			
				data = database.getDataFromAsigId( x )
				rows = rows + "<tr>" + ( _row % ( database.getAuthorFromAsigId( x ) ) +
										_row % ( database.getWPFromAsigId( x ) ) +
										_row % ( database.getAsFromAsigId( x ) ) +
										'\n'.join( [ _row % ( y ) for y in data ] ) +
										_row % (( """<p><button onclick='editrow(%d)' class='btn btn-primary btn-mini'>Editar</button></p>""" ) % ( x ) +
											  """<button onclick='deleterow(%d)' class='btn btn-primary btn-mini'>Borrar</button>""" % ( x ) ) +
											  "</tr>")
			else:
				rows = rows + _lineToEdit

		return [_header % ("Lista de asignaciones"), _body % (rows), "<div><a href = '/'>Regresar</a></div> " ,_footer ]
	asiglist.exposed = True

	def borrarlinea( self, row ):
		database = db.database("basedatosCAP.db")
		database.deleteRow( int(row) )
		raise cherrypy.HTTPRedirect("/asiglist")
	borrarlinea.exposed = True

# Starts the webpage
if __name__ == '__main__':
	current_dir = os.path.dirname( os.path.abspath(__file__) )
	ip   = os.environ['OPENSHIFT_PYTHON_IP']
	port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
	#port = 8000
	#ip = "127.0.0.1"

	http_conf = {'global': {'server.socket_port': port,
									'server.socket_host': ip}}
	cherrypy.config.update(http_conf)

	conf = {'/style.css':{'tools.staticfile.on':True, 
			  					 'tools.staticfile.filename':current_dir+"/style.css"},
			  '/some.js':{'tools.staticfile.on':True,
			  				  'tools.staticfile.filename':current_dir+"/some.js"}}
	

	cherrypy.quickstart( HelloWorld(), "/", config = conf )

#=========================================================================================

