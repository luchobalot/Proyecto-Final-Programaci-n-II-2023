from flask import Blueprint, jsonify, request
from Modelos.agenda_medicos import obtener_horarios_ordenados, agregar_horario_medico, modificar_horario_medico, eliminar_dias_atencion_medico

# Se crea un objeto Blueprint.
agenda_bp = Blueprint("agenda", __name__)

# ==================================
#|    OBTENER LA AGENDA ORDENADA   |
# ==================================

# Ruta para obtener la agenda de manera ordenada
@agenda_bp.route('/agenda_medicos', methods=['GET'])
def obtener_agenda():
    agenda_ordenada = obtener_horarios_ordenados()
    return jsonify(agenda_ordenada)


# ==================================
#| AGREGAR DIA Y HORARIO A AGENDA  |
# ==================================

# Ruta para agregar un dIa y horario de atención a un mdico.
@agenda_bp.route('/agenda_medicos', methods=['POST'])
def agregar_horario():
    datos_nuevo_horario = request.get_json()

    id_medico = datos_nuevo_horario.get('id_medico')
    dia_numero = datos_nuevo_horario.get('dia_numero')
    hora_inicio = datos_nuevo_horario.get('hora_inicio')
    hora_fin = datos_nuevo_horario.get('hora_fin')

    if id_medico and dia_numero and hora_inicio and hora_fin:
        exito = agregar_horario_medico(id_medico, dia_numero, hora_inicio, hora_fin)

        if exito:
            return jsonify({"Mensaje": "Día y horario de trabajo agregados correctamente!"}), 201
        else:
            return jsonify({"Error": "El medico ya tiene este horario de trabajo asignado."}), 400
    else:
        return jsonify({"Error": "Faltan datos en la solicitud."}), 400


# ==================================
#| MODIFICAR HORARIO EN LA AGENDA  |
# ==================================

# Ruta que permite modificar un horario de atencion en la agenda (Horario, dia, etc)

# Para que funcione correctamente, en Postman poner bien los parametros para indicar exactamente cual es el horario a modificar.
@agenda_bp.route('/modificar_horario', methods=['PUT'])
def modificar_horario():
    datos_modificacion = request.get_json()

    id_medico = datos_modificacion.get('id_medico')
    dia_numero = datos_modificacion.get('dia_numero')
    hora_inicio_actual = datos_modificacion.get('hora_inicio_actual')
    hora_fin_actual = datos_modificacion.get('hora_fin_actual')
    hora_inicio_nueva = datos_modificacion.get('hora_inicio_nueva')
    hora_fin_nueva = datos_modificacion.get('hora_fin_nueva')

    if id_medico and dia_numero and hora_inicio_actual and hora_fin_actual and hora_inicio_nueva and hora_fin_nueva:
        exito = modificar_horario_medico(
            id_medico,
            dia_numero,
            hora_inicio_actual,
            hora_fin_actual,
            hora_inicio_nueva,
            hora_fin_nueva
        )

        if exito:
            return jsonify({"mensaje": "Horario modificado correctamente"}), 200
        else:
            return jsonify({"mensaje": "No se encontró el horario para modificar"}), 404
    else:
        return jsonify({"mensaje": "Faltan datos en la solicitud"}), 400


# ==================================
#|     ELIMINAR DIA DE ATENCIÓN    |
# ==================================

# Ruta que permite eliminar todos los días de atención de un médico por su ID.
@agenda_bp.route('/eliminar_dias_atencion/<int:id_medico>', methods=['DELETE'])
def eliminar_dias_atencion(id_medico):
    eliminado = eliminar_dias_atencion_medico(id_medico)

    if eliminado:
        return jsonify({"mensaje": f"Días de atencin del medico con ID: {id_medico} se eliminaron correctamente."}), 200
    else:
        return jsonify({"Error": f"No se encontraron dias de atencion para el médico con ID: {id_medico}"}), 404