import sqlite3 as sqlite

class database:
	def __init__(self, dbname):
		self.con = sqlite.connect(dbname)

	def __del__(self):
		self.con.close()

	def dbcommit( self ):
		self.con.commit()

	def insertData( self, query ):
		self.con.execute( query )
		self.con.commit()

	def getNames( self, table ):
		name = self.con.execute( "select nombre from %s" % (table) )
		return [ x[0] for x in name ]

	def getId( self, table, name ):
		id = self.con.execute( "select rowid from %s where nombre = '%s'" % ( table, name ) )
		id = id.fetchone()[0]
		return id

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
		return data.fetchall()

	def deleteRow( self, asigId ):
		self.con.execute( "delete from asignaciones where rowid = %d" % ( asigId ) )
		self.con.commit()