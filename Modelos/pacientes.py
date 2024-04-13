import requests
from flask import request, jsonify
import csv

# Se importan algunas funciones del archivo turnos
from Modelos.turnos import cargar_turnos_desde_csv

# ======================================
# |             PACIENTES              |
# ======================================

# Se define la URL de la API
url = "https://randomuser.me/api"

lista_de_pacientes = [] # Lista que almacenara los pacientes.
contador_id_pacientes = 0

def cargar_pacientes_desde_csv():
    ruta_csv = "Modelos/pacientes.csv"

    global contador_id_pacientes, lista_de_pacientes
    
    lista_de_pacientes = []
    
    try:
        with open(ruta_csv, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                id_paciente = int(row['id'])
                contador_id_pacientes = max(contador_id_pacientes, id_paciente)
                # Convierte 'row' a un diccionario
                paciente_dict = dict(row)
                lista_de_pacientes.append(paciente_dict)
    except FileNotFoundError:
        pass
    return lista_de_pacientes  
    
cargar_pacientes_desde_csv()


# Función para generar pacientes.
def generar_pacientes():
    global contador_id_pacientes, lista_de_pacientes
    
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200: # Se verifica si la solicitud fue exitosa.
        datos_paciente = respuesta.json()['results'][0]
        
        paciente = {
            'id': contador_id_pacientes + 100,
            'dni': datos_paciente['id']['value'],
            'nombre': datos_paciente['name']['first'],
            'apellido': datos_paciente['name']['last'],
            'telefono': datos_paciente['phone'],
            'email': datos_paciente['email'],
            'direccion_calle': datos_paciente['location']['street']['name'],
            'direccion_numero': datos_paciente['location']['street']['number']
        }
            
        contador_id_pacientes += 1
        lista_de_pacientes.append(paciente)
        
        exportar_csv()
        return paciente
    return None


# Función para obtener un paciente por su ID.
def obtener_paciente_id(paciente_id):
    for paciente in lista_de_pacientes:
        if int(paciente['id']) == paciente_id: # El int asegura que ambas variables tengan el mismo tipo de datos y que la comparacion sea correcta.
            return paciente
    # En caso de no encontrar al paciente devuelve None.
    return None


# Función para modificar información/datos de un paciente por su ID.
def editar_paciente_id(paciente_id, dni, nombre, apellido, telefono, email, direccion_calle, direccion_numero):
    for paciente in lista_de_pacientes:
        if int(paciente['id']) == paciente_id:
            paciente["dni"] = dni
            paciente["nombre"] = nombre
            paciente["apellido"] = apellido
            paciente["telefono"] = telefono
            paciente["email"] = email
            paciente["direccion_calle"] = direccion_calle
            paciente["direccion_numero"] = direccion_numero

            exportar_csv()
            return paciente
    # En caso de no encontrar al paciente, devuelve None.
    return None

# Funciones para eliminar un paciente por su ID:
# Funcion que verifica si el paciente tiene turnos asignados.
def paciente_turnos_pendientes(paciente_id):
    turnos = cargar_turnos_desde_csv()
    
    for turno in turnos:
        if int(turno['id_paciente']) == paciente_id:
            return True
    
    return False

# Funcion para eliminar paciene (Siempre y cuando no tenga turnos)
def eliminar_paciente(paciente_id):
    global lista_de_pacientes
    
    if paciente_turnos_pendientes(paciente_id):
        return None  # Devueve None si el paciente tiene turnos pendientes y no puede ser eliminado.
    
    for i, paciente in enumerate(lista_de_pacientes):
        if int(paciente['id']) == paciente_id:
            paciente_eliminado = lista_de_pacientes.pop(i)
            
            exportar_csv()
            return paciente_eliminado
    
    return None # Em caso de que no se encuenttre el paciente.













    
# Función para exportar los datos generados al archivo CSV.
def exportar_csv():
    
    # Ruta completa del archivo CSV
    ruta_csv = "Modelos/pacientes.csv"
    
    # Encabezado del archivo CSV
    encabezados_pacientes = ['id', 'dni', 'nombre', 'apellido', 'telefono', 'email', 'direccion_calle', 'direccion_numero']
    
    with open(ruta_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=encabezados_pacientes)
        writer.writeheader()
        writer.writerows(lista_de_pacientes)