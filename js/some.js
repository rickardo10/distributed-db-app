
//FUNCIONES FORMAS/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function onChangeSetVar(){
	var x = document.getElementById("invest");
	window.location.href="asignartarea?investigador="+x.value
}

function deleterow( row ){
	window.location.href="borrarlinea?row="+row
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
    $("#myTable").tableFilter();
    $("table").tablesorter({ 
    // pass the headers argument and assing a object 
        headers: { 
            0: { 
                // disable it by setting the property sorter to false 
                sorter: false 
            }, 
            // assign the secound column (we start counting zero) 
            1: { 
                // disable it by setting the property sorter to false 
                sorter: false 
            }, 
            // assign the third column (we start counting zero) 
            2: { 
                // disable it by setting the property sorter to false 
                sorter: false 
            }, 
            3: { 
                // disable it by setting the property sorter to false 
                sorter: false 
            }, 
            // assign the secound column (we start counting zero) 
            4: { 
                // disable it by setting the property sorter to false 
                sorter: false 
            }, 
            // assign the third column (we start counting zero) 
            5: { 
                // disable it by setting the property sorter to false 
                sorter: false 
            },
                6: { 
                // disable it by setting the property sorter to false 
                sorter: false 
            }, 
            7: { 
                // disable it by setting the property sorter to false 
                sorter: false
            }, 
            // assign the secound column (we start counting zero) 
            8: { 
                // disable it by setting the property sorter to false 
                sorter: false 
            }, 
            // assign the third column (we start counting zero) 
            
            9: { 
                // disable it by setting the property sorter to false 
                sorter: false 
            }, 
            10: { 
                // disable it by setting the property sorter to false 
                sorter: false 
            }
        } 
    }); 
});