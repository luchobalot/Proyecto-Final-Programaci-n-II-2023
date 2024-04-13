import csv
from datetime import datetime
from flask import jsonify

# ======================================
# |               TURNOS               |
# ======================================

# Ruta del archivo CSV para los turnos.
ruta_csv_turnos = "Modelos/turnos.csv"

# Función para cargar los turnos desde el archivo CSV.
def cargar_turnos_desde_csv():
    try:
        with open(ruta_csv_turnos, 'r', newline='', encoding='utf-8') as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            turnos = list(lector_csv)
        return turnos
    except FileNotFoundError:
        return []


# Funcin para exportar los turnos al archivo CSV.
def exportar_csv_turnos(turnos):
    # Encabezado del archivo CSV
    encabezados = ['id_medico', 'id_paciente', 'hora_turno', 'fecha_solicitud']

    with open(ruta_csv_turnos, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=encabezados)
        writer.writeheader()
        writer.writerows(turnos)
        

# Función para obtener los turnos de un médico por su ID.
def obtener_turnos_por_medico(id_medico):
    turnos = cargar_turnos_desde_csv()
    turnos_medico = [turno for turno in turnos if int(turno['id_medico']) == id_medico]
    return turnos_medico


# Función para registrar un nuevo turno.
def registrar_turno(id_medico, id_paciente, hora_turno):
    # Obtener la fecha de solicitud en el formato deseado.
    fecha_solicitud = datetime.now().strftime('%Y/%m/%d')

    turnos = cargar_turnos_desde_csv()

    nuevo_turno = {
        'id_medico': id_medico,
        'id_paciente': id_paciente,
        'hora_turno': hora_turno,
        'fecha_solicitud': fecha_solicitud
    }
    turnos.append(nuevo_turno)
    exportar_csv_turnos(turnos)

    return nuevo_turno


# Función para anular un turno por el ID del paciente.
def anular_turno_id(id_paciente):
    turnos = cargar_turnos_desde_csv()
    turno_anulado = None

    for turno in turnos:
        if int(turno['id_paciente']) == id_paciente:
            turno_anulado = turno
            break

    if turno_anulado:
        turnos = [t for t in turnos if int(t['id_paciente']) != id_paciente]
        exportar_csv_turnos(turnos)
        return jsonify({'Mensjae': 'Turno anulado correctamente.', 'Turno eliminado': turno_anulado})
    else:
        return jsonify({'Error': 'Turno no encontrado.'}), 404
