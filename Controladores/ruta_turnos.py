from flask import Blueprint, jsonify, request

from Modelos.turnos import obtener_turnos_por_medico, registrar_turno, anular_turno_id


# Se crea un objeto Blueprint.
turnos_bp = Blueprint("turnos", __name__)

# ======================================
# |     OBTENER TODOS LOS TURNOS       |
# ====================================== 

# Ruta para obtener todos los turnos de un médico por su ID (GET).
@turnos_bp.route('/turnos/<int:id_medico>', methods=['GET'])
def obtener_turnos(id_medico):
    turnos_medico = obtener_turnos_por_medico(id_medico)

    if turnos_medico:
        return jsonify(turnos_medico)
    else:
        # En caso de que no haya un medico generado o no tenga turnos asignaods:
        return jsonify({"Error": "No se encontraron turnos asignados el médico con ID: {}".format(id_medico)}), 404
    

# ======================================
# |        REGISTRAR NUEVO TURNO       |
# ====================================== 

# Ruta para registrar un nuevo turno (POST).
@turnos_bp.route('/generar_turno', methods=['POST'])
def agregar_turno():
    if request.is_json:
        datos_turno = request.get_json()

        if 'id_medico' in datos_turno and 'id_paciente' in datos_turno and 'hora_turno' in datos_turno:
            nuevo_turno = registrar_turno(
                id_medico=datos_turno['id_medico'],
                id_paciente=datos_turno['id_paciente'],
                hora_turno=datos_turno['hora_turno']
            )
            return jsonify(nuevo_turno), 201
        else:
            return jsonify({"Error": "Datos incompletos para registrar el turno."}), 400
    else:
        return jsonify({"Eror": "No se recibio formato JSON."}), 400


# ======================================
# |         ELIMINAR UN TURNO          |
# ======================================    
    
# Ruta para registrar la anulación de un turno por el ID del paciente.
@turnos_bp.route('/turnos/<int:id_paciente>', methods=['DELETE'])
def anular_turno(id_paciente):
    return anular_turno_id(id_paciente)
