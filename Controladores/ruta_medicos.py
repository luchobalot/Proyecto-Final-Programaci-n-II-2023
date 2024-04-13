from flask import Blueprint, jsonify, request
import csv

from Modelos.medicos import generar_medicos, obtener_medico_id, editar_medico_id, deshabilitar_medico

# Se crea un objeto Blueprint.
medicos_bp = Blueprint("medicos", __name__)

# Ruta para generar médicos.
@medicos_bp.route('/generar_medicos', methods=['POST'])
def generar_lista_medicos():
    global lista_de_medicos
    cantidad_medicos = 15  # Ajustar la cantidad segun sea necesario
    
    medicos_generados = [generar_medicos() for _ in range(cantidad_medicos)]
     
    lista_de_medicos = [medico for medico in medicos_generados if medico is not None]
    
    return jsonify(lista_de_medicos)


# ======================================
# | OBTENER LISTA DE TODOS LOS MEDICOS |
# ======================================

# Ruta para obtener la lista de todos los médicos desde el archivo CSV.
@medicos_bp.route('/lista_medicos', methods=['GET'])
def obtener_lista_de_medicos_desde_csv():
    
    # Ruta completa del archivo CSV
    ruta_csv = "Modelos/medicos.csv"
    
    try:
        with open(ruta_csv, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            medicos = list(reader)
            
        return jsonify(medicos), 200
    
    # En caso de que haya errores al abrir el archivo CSV.
    except FileNotFoundError:
        return jsonify({'Error': 'Archivo CSV no encontrado.'}), 404
    
    except Exception as e:
        return jsonify({'Error': 'Error al leer el archivo CSV.'}), 500
    

# ======================================
# |  OBTENER DETALLE MEDICO POR SU ID  |
# ======================================

# Ruta para obtener los detalles de un médico por su ID.
@medicos_bp.route('/medicos/<int:medico_id>', methods=['GET'])
def obtener_medico_por_id(medico_id):
    # Llama a la función obtener_medico_id
    medico = obtener_medico_id(medico_id)

    if medico:
        return jsonify(medico)
    else:
        return jsonify({"Error": "Medico no encontrado"}), 404


# ======================================
# |  AGREGAR UN NUEVO MEDICO - RANDOM  |
# ======================================

# Ruta para agregar un médico (Genera un medico random con la API).
@medicos_bp.route('/medicos', methods=['POST'])
def agregar_medico():
    # Llama a la función generar_medicos para obtener un nuevo médico.
    nuevo_medico = generar_medicos()

    # Verifica si se generó correctamente el nuevo médico.
    if nuevo_medico:
        return jsonify(nuevo_medico), 201
    else:
        return jsonify({"Error": "No se puedo generar un nuevo medico."}), 500
    
    
# ======================================
# |   ACTUALIZAR INFORMACIÓN MEDICO    |
# ======================================

# Ruta para modificar los datos de un médico por su ID.
@medicos_bp.route('/medicos/<int:medico_id>', methods=['PUT'])
def modificar_medico(medico_id):
    if request.is_json:
        
        nuevos_datos = request.get_json()
        if 'dni' in nuevos_datos and 'nombre' in nuevos_datos and 'apellido' in nuevos_datos and 'matricula' in nuevos_datos and 'telefono' in nuevos_datos and 'email' in nuevos_datos:
            
            medico_modificado = editar_medico_id(medico_id, nuevos_datos['dni'], nuevos_datos['nombre'], nuevos_datos['apellido'], nuevos_datos['matricula'], nuevos_datos['telefono'], nuevos_datos['email'])
            
            if medico_modificado:
                return jsonify(medico_modificado)
            else:
                return jsonify({'Error': 'El médico no se ha encontrado.'}), 404
        else:
            return jsonify({'Error': 'Faltan datos para poder editar el médico.'}), 400
    else:
        return jsonify({'Error': 'No se recibió el formato JSON.'}), 400
    
    
# ======================================
# |      DESHABILITAR UN MEDICO        |
# ======================================

# Ruta para deshabilitar un medico por su ID.
@medicos_bp.route('/medicos/deshabilitar/<int:medico_id>', methods=['PUT'])
def deshabilitar_un_medico(medico_id):
    medico_deshabilitado = deshabilitar_medico(medico_id)

    if medico_deshabilitado:
        return jsonify({"Mensaje": f"El medico con ID {medico_id} se deshabilito correctamente."})
    else:
        return jsonify({"Error": f"No se encontr al médico con ID {medico_id}."}), 404



