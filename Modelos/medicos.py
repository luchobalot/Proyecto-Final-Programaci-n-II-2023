import requests
from flask import request, jsonify
import csv

# ======================================
# |              MEDICOS               |
# ======================================

# Se define la URL de la API
url = "https://randomuser.me/api"

lista_de_medicos = [] # Lista que almacenara los médicos.
contador_id_medicos = 0

def cargar_medicos_desde_csv():
    ruta_csv = "Modelos/medicos.csv"
    
    try:
        with open(ruta_csv, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            
            global contador_id_medicos
            
            for row in reader:
                contador_id_medicos = max(contador_id_medicos, int(row['id']))
                lista_de_medicos.append(row)
    except FileNotFoundError:
        pass
    
cargar_medicos_desde_csv()

# Función para generar los médicos.
def generar_medicos():
    global contador_id_medicos, lista_de_medicos
    
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200: # Se verifica si la solicitud fue exitosa.
        datos_medicos = respuesta.json()['results'][0]
        
        medico= {
                'id': contador_id_medicos + 1,
                'dni': datos_medicos['id']['value'],
                'nombre': datos_medicos['name']['first'],
                'apellido': datos_medicos['name']['last'],
                'matricula': datos_medicos['login']['password'],
                'telefono': datos_medicos['phone'],
                'email': datos_medicos['email'],
                'habilitado': True
            }
            
        contador_id_medicos += 1
        lista_de_medicos.append(medico)
        exportar_csv()
        return medico
    return None


# Función para obtener un médico por su ID.
def obtener_medico_id(medico_id):
    for medico in lista_de_medicos:
        if int(medico['id']) == medico_id: # El int asegura que ambas variables tengan el mismo tipo de datos y que la comparacion sea correcta.
            return medico
    # En caso de no encontrar al médico devuelve None.
    return None


# Función para modificar información/datos de un médico por su ID.
def editar_medico_id(medico_id, dni, nombre, apellido, matricula, telefono, email):
    for medico in lista_de_medicos:
        if int(medico['id']) == medico_id:
            
            medico["dni"] = dni
            medico["nombre"] = nombre
            medico["apellido"] = apellido
            medico["matricula"] = matricula
            medico["telefono"] = telefono
            medico["email"] = email
            
            exportar_csv()
            return medico
    # En caso de no encontrar al médico devuelve None.
    return None


# Función para deshabilitar un médico por su ID.
def deshabilitar_medico(medico_id):
    global lista_de_medicos
    
    for medico in lista_de_medicos:
        if int(medico['id']) == medico_id:
            medico["habilitado"] = False
            exportar_csv()
            return medico
    
    return None


# Función para exportar los datos generados al archivo CSV.
def exportar_csv():
    # Ruta completa del archivo CSV
    ruta_csv = "Modelos/medicos.csv"
    
    # Encabezado del archivo CSV
    encabezados = ['id', 'dni', 'nombre', 'apellido', 'matricula', 'telefono', 'email', 'habilitado']
    
    with open(ruta_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=encabezados)
        writer.writeheader()
        writer.writerows(lista_de_medicos)