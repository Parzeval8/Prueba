
// Función para obtener el token CSRF
function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

// Función para actualizar una tarea
function updateTask(checkbox) {
    var taskId = checkbox.id.split('-')[2];
    var done = checkbox.checked;

    // Obtener la fecha y hora actual en formato ISO 8601
    var tzoffset = (new Date()).getTimezoneOffset() * 60000; //offset in milliseconds
    var now = (new Date(Date.now() - tzoffset)).toISOString().slice(0, -1);
    $.ajax({
        type: "POST",
        url: "{% url 'update_done' %}",
        data: {
            csrfmiddlewaretoken: getCSRFToken(),
            task_id: taskId,
            done: done,
            date_completed: now
        },
        success: function(response) {
            if (response.success) {
                checkbox.checked = response.done;
                // Llama a la función para resaltar tareas vencidas
                highlightOverdueTasks();
                var dateCompletedCell = document.getElementById('date-completed-' + taskId);
                if (response.done) {
                    var dateCompleted = new Date(response.date_completed);
                    dateCompletedCell.innerText = dateCompleted.toLocaleString('en-US', { month: 'short', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true });
                    checkbox.closest('tr').classList.add('table-success');
                } else {
                    dateCompletedCell.innerText = '';
                    checkbox.closest('tr').classList.remove('table-success');
                }
            } else {
                console.error('Error al actualizar el estado de la tarea.');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error de solicitud AJAX:', error);
        }
    });
}

// Función para resaltar tareas vencidas
function highlightOverdueTasks() {
    console.log('hello')
    var rows = document.querySelectorAll('tbody tr'); // Obtener todas las filas de la tabla
    var currentDate = new Date(); // Obtener la fecha actual

    rows.forEach(function(row) {
        var dueDateCell = row.querySelector('.due-date'); // Obtener la celda de la fecha de vencimiento
        var doneCell = row.querySelector('.done'); // Obtener la celda de la tarea realizada
        if (doneCell.checked) {
            row.classList.add('table-success'); // Agregar la clase 'table-success' para marcar la fila en verde
            row.classList.remove('table-danger');
        } else if (dueDateCell) {
            var dueDateText = dueDateCell.textContent.trim(); // Obtener el texto de la celda y eliminar espacios en blanco
            var dueDate = parseDate(dueDateText); // Convertir el texto de la fecha en un objeto de fecha
            if (dueDate < currentDate) {
                row.classList.remove('table-success');
                row.classList.add('table-danger'); // Agregar la clase 'table-danger' para marcar la fila en rojo
            }
        }
    });
}

// Función para convertir el texto de la fecha en un objeto de fecha
function parseDate(dateText) {
    // Utilizar expresiones regulares para extraer las partes de la fecha y hora
    var regex = /(\w+)\. (\d+), (\d+), (\d+):(\d+)\s([apAP]\.m\.)/;
    var match = regex.exec(dateText);
    if (match === null) {
        console.error('Formato de fecha no válido:', dateText);
        return null;
    }

    var month = match[1];
    var day = parseInt(match[2]);
    var year = parseInt(match[3]);
    var hour = parseInt(match[4]);
    var minute = parseInt(match[5]);        
    var ampm = match[6].toLowerCase();

    // Convertir la hora al formato de 24 horas si es necesario
    if (ampm === 'p.m.' && hour < 12) {
        hour += 12;
    } else if (ampm === 'a.m.' && hour === 12) {
        hour = 0;
    }

    // Convertir el nombre del mes a su número de índice
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var monthIndex = months.indexOf(month);

    // Crear un objeto de fecha en formato ISO 8601
    var isoDateString = year + '-' + pad(monthIndex + 1, 2) + '-' + pad(day, 2) + 'T' + pad(hour, 2) + ':' + pad(minute, 2) + ':00';
    var date = new Date(isoDateString);

    return date;
}

// Función para rellenar ceros a la izquierda si es necesario
function pad(number, length) {
    var str = String(number);
    while (str.length < length) {
        str = '0' + str;
    }
    return str;
}

//Ordenar la tabla de tareas
function sortTasks(option) {
    var rows = Array.from(document.querySelectorAll('#task-table tbody tr'));
    var sortedRows = rows.sort(function(a, b) {
        var valueA, valueB;
        if (option === 'priority') {
            var priorityCellA = a.querySelector('.priority');
            var priorityCellB = b.querySelector('.priority');
            valueA = getPriorityValue(priorityCellA.textContent.trim());
            valueB = getPriorityValue(priorityCellB.textContent.trim());
            console.log('a '+(valueA - valueB))
            return valueA - valueB;
        } else if (option === 'due-date') {
            valueA = new Date(a.querySelector('.due-date').textContent);
            valueB = new Date(b.querySelector('.due-date').textContent);
            return valueA - valueB;
        } else if (option === 'title') {
            valueA = a.querySelector('td:first-child').textContent;
            valueB = b.querySelector('td:first-child').textContent;
            return valueA.localeCompare(valueB);
        }
        
    });

    var tbody = document.querySelector('#task-table tbody');
    sortedRows.forEach(function(row) {
        tbody.appendChild(row);
    });
}

function getPriorityValue(priorityText) {
    switch (priorityText) {
        case 'Lowest':
            return 5;
        case 'Low':
            return 4;
        case 'Normal':
            return 3;
        case 'High':
            return 2;
        case 'Highest':
            return 1;
        default:
            return 0;
    }
}

// Llamadas a funciones cuando se carga la página
window.addEventListener('DOMContentLoaded', function() {
    document.getElementById('sort-select').addEventListener('change', function() {
        sortTasks(this.value);
    }); // Ordena inicialmente las tareas por título
    highlightOverdueTasks(); // Resalta las tareas vencidas
});
setInterval(highlightOverdueTasks, 60000);