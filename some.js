
//FUNCIONES FORMAS/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function onChangeSetVar(){
	var x = document.getElementById("invest");
	window.location.href="asignartarea?investigador="+x.value
}

function editrow( row ){
	window.location.href="asiglist?row="+row
}

function guardar( row ){
	var comment = document.getElementById("comment").value
	var asignado = document.getElementById("asignado").value
	var avance = document.getElementById("avance").value
	var prioridad = document.getElementById("prioridad").value
	var estado = document.getElementById("estado").value
	window.location.href="updaterow?row="+row+"&comentarios="+comment+"&asignado="+asignado+"&avance="+avance+"&prioridad="+prioridad+"&estado="+estado
}

function terminado( row ){
	window.location.href="terminado?row="+row
}

//SORTER///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// sets initial sort
$(document).ready(function() { 
    $("#myTable").tablesorter( {sortList: [[4,0], [5,0], [7,0]]} );
    $("table").tablesorter({ 
    // pass the headers argument and assing a object 
        headers: {  { x:{sorter:false } for x in range(11) }
        } 
    }); 
});