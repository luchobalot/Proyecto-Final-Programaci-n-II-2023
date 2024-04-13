from flask import Blueprint, jsonify, request
import csv

from Modelos.pacientes import generar_pacientes, obtener_paciente_id, editar_paciente_id, cargar_pacientes_desde_csv, eliminar_paciente, paciente_turnos_pendientes

# Se crea un objeto Blueprint.
pacientes_bp = Blueprint("pacientes", __name__)

# Ruta para generar pacientes.
@pacientes_bp.route('/generar_pacientes', methods=['POST'])
def generar_lista_pacientes():
    global lista_de_pacientes
    
    cantidad_pacientes = 15  # Ajustar la cantidad segun sea necesario
    
    pacientes_generados = [generar_pacientes() for _ in range(cantidad_pacientes)]
     
    lista_de_pacientes = [paciente for paciente in  pacientes_generados if paciente is not None]
    
    return jsonify(lista_de_pacientes)


# ========================================
# | OBTENER LISTA DE TODOS LOS PACIENTES |
# ========================================

# Ruta para obtener la lista de todos los pacientes desde el archivo CSV.
@pacientes_bp.route('/pacientes', methods=['GET'])
def obtener_lista_pacientes():
    try:
        pacientes = cargar_pacientes_desde_csv()
        return jsonify(pacientes), 200

    # En caso de que haya errores al abrir el archivo CSV.
    except FileNotFoundError:
        return jsonify({'Error': 'Archivo CSV no encontrado.'}), 404

    except Exception as e:
        return jsonify({'Error': 'Error al leer el archivo CSV.'}), 500


# ========================================
# |  OBTENER DETALLE PACIENTE POR SU ID  |
# ========================================

# Ruta para obtener los detalles de un médico por su ID.
@pacientes_bp.route('/pacientes/<int:paciente_id>', methods=['GET'])
def obtener_paciente_por_id(paciente_id):
    paciente = obtener_paciente_id(paciente_id)

    if paciente:
        return jsonify(paciente)
    else:
        return jsonify({"Error": "Paciente no encontrado"}), 404
    
    
# ======================================
# |  ACTUALIZAR INFORMACIÓN PACIENTE   |
# ======================================

# Ruta para modificar los datos de un paciente por su ID.
@pacientes_bp.route('/pacientes/<int:paciente_id>', methods=['PUT'])
def modificar_paciente(paciente_id):
    if request.is_json:
        
        nuevos_datos = request.get_json()
        if 'dni' in nuevos_datos and 'nombre' in nuevos_datos and 'apellido' in nuevos_datos and 'telefono' in nuevos_datos and 'email' in nuevos_datos and 'direccion_calle' in nuevos_datos and 'direccion_numero' in nuevos_datos:
            
            paciente_modificado = editar_paciente_id(paciente_id, nuevos_datos['dni'], nuevos_datos['nombre'], nuevos_datos['apellido'], nuevos_datos['telefono'], nuevos_datos['email'], nuevos_datos['direccion_calle'], nuevos_datos['direccion_numero'])
            
            if paciente_modificado:
                return jsonify(paciente_modificado)
            else:
                return jsonify({'Error': 'El paciente no se ha encontrado.'}), 404
        else:
            return jsonify({'Error': 'Faltan datos para poder editar el paciente.'}), 400
    else:
        return jsonify({'Error': 'No se recibió el formato JSON.'}), 400


# ========================================
# |  AGREGAR UN NUEVO PACIENTE - RANDOM  |
# ========================================

# Ruta para agregar un paciente (Genera un nuevo paciente random con la API).
@pacientes_bp.route('/nuevo_paciente', methods=['POST'])
def agregar_paciente():
    
    nuevo_paciente = generar_pacientes()

    # Verifica si se gener correctamente un nuevo paciente.
    if nuevo_paciente:
        return jsonify(nuevo_paciente), 201
    else:
        return jsonify({"Error": "No se pudo generar un nuevo paciente."}), 500


# ======================================
# |        ELIMINAR UN PACIENTE        |
# ======================================

# Ruta para eliminar un paciente por su ID
@pacientes_bp.route('/pacientes/<int:paciente_id>', methods=['DELETE'])
def borrar_paciente(paciente_id):
    paciente_eliminado = eliminar_paciente(paciente_id)

    if paciente_eliminado:
        return jsonify({"Mensaje": f"El paciente con ID {paciente_id} se elimino correctamente."})
    
    elif paciente_turnos_pendientes(paciente_id):
        return jsonify({"Error": f"No se puede eliminar el paciente con ID {paciente_id}, tiene turnos pendientes."}), 400
    else:
        return jsonify({"Error": f"No se encontro al paciente con ID {paciente_id}."}), 404
