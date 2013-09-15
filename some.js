function onChangeSetVar(){
	var x = document.getElementById("invest");
	window.location.href="asignartarea?investigador="+x.value
}

function deleterow( row ){
	window.location.href="borrarlinea?row="+row
}

function editrow( row ){
	var comments = document.getElementById("comment")
	alert(row)
}