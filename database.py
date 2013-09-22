import sqlite3 as sqlite

class database:
	def __init__(self, dbname):
		self.con = sqlite.connect(dbname)

	def __del__(self):
		self.con.close()

	def dbcommit( self ):
		self.con.commit()

	def insertData( self, query ):
		result = self.con.execute( query )
		self.con.commit()
		return result

	def getNames( self, table ):
		name = self.con.execute( "select nombre from %s" % (table) )
		return [ x[0] for x in name ]

	def getIds( self, table ):
		name = self.con.execute( "select rowid from %s" % (table) )
		return [ x[0] for x in name ]

	def getId( self, table, name ):
		id = self.con.execute( "select rowid from %s where nombre = '%s'" % ( table, name ) )
		id = id.fetchone()[0]
		return id

	def getName( self, table, name ):
		name = self.insertData( "select nombre from %s where rowid = %s" % ( table, name ) )
		return name.fetchone()[0]

	def getIdWP( self, name ):
		id = self.con.execute( "select rowid from workingpaper where nombrewp = '%s'" % ( name ) )
		id = id.fetchone()[0]
		return id

	def getIdAsig( self, descripcion ):
		id = self.con.execute( "select rowid from asignaciones where descripcion = '%s'" % (descripcion) ) 
		id = id.fetchone()[0]
		return id

	def getWorkingPapers( self, nameId ):
		workingPaper = self.con.execute( (  "select nombrewp from workingpaper where rowid in ( select wpid from linkworkingpaper where invid = %d )" ) % nameId )
		workingPaper = [ x[0] for x in workingPaper ]
		return workingPaper

	def getWpIds( self ):
		wp = self.con.execute( "select rowid from workingpaper")
		return [ x[0] for x in wp ]

	def getAsignments( self, nameIds ):
		Asignments = self.con.execute( (  "select rowid from asignaciones where rowid in ( select asigid from linkasignaciones where asid = %d )" ) % nameIds )
		Asignments = [ x[0] for x in Asignments ]
		return Asignments

	def getAuthorFromAsigId( self, asigId ):
		Asignments = self.con.execute( (  "select nombre from investigador where rowid = ( select invid from linkworkingpaper where wpid = ( select wpid from linkasignaciones where asigid = %d ) )" ) % ( asigId ) )
		Asignments = Asignments.fetchone()[0]
		return Asignments

	def getWPFromAsigId( self, asigId ):
		WP = self.con.execute( "select nombrewp from workingpaper where rowid in ( select wpid from linkasignaciones where asigid = %d )" % (asigId ) )
		WP = WP.fetchone()[0]
		return WP

	def getAsFromAsigId( self, asigId ):
		WP = self.con.execute( "select nombre from asistente where rowid = ( select asid from linkasignaciones where asigid = %d )" % ( asigId ) )
		WP = WP.fetchone()[0]
		return WP

	def getDataFromAsigId( self, asigId ):
		data = self.con.execute( "select * from asignaciones where rowid = %d " % ( asigId ) )
		return data.fetchall()[0]

	def getAsigFromWpAndInv( self, invId, wpId ):
		asigs = self.con.execute( "select A.rowid from linkasignaciones as A join linkworkingpaper as B on B.wpid = A.wpid where B.invid = %d and A.wpid = %d" % ( invId, wpId ) )
		return [ x[0] for x in asigs ]

	def deleteRow( self, asigId ):
		self.con.execute( "delete from asignaciones where rowid = %d" % ( asigId ) )
		self.con.execute( "delete from linkasignaciones where asigid = %d" % (asigId) )
		self.con.commit()

	def updateRow( self, asigId, asignado, estado, prioridad, avance, comentarios ):
		self.con.execute( "update linkasignaciones set asid = '%d' where asigId = %d" % (asignado, asigId ) )
		self.con.execute( "update asignaciones set estatus = '%s' where rowid = %d" % (estado, asigId ) )
		self.con.execute( "update asignaciones set prioridad = '%s' where rowid = %d" % (prioridad, asigId ) )
		self.con.execute( "update asignaciones set avance = '%s' where rowid = %d" % (avance, asigId ) )
		self.con.execute( "update asignaciones set comentarios = '%s' where rowid = %d" % (comentarios, asigId ) )
		self.con.commit()