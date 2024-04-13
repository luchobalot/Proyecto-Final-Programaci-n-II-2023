import csv
from datetime import datetime

# ======================================
# |          AGENDA DE MEDICOS         |
# ======================================

# Nombre del archivo CSV para la agenda de médicos.
ruta_csv_agenda = "Modelos/agenda_medicos.csv"

# Función para cargar la agenda de médicos desde el archivo CSV
def cargar_agenda_medicos():
   with open(ruta_csv_agenda, 'r', newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        return list(lector_csv)


# Funcion parw exportar los datos al archivo CSV.
def exportar_csv_agenda(agenda_medicos):
    # Encabezado del archivo CSV
    encabezados = ['id_medico', 'dia_numero', 'hora_inicio', 'hora_fin', 'fecha_actualizacion']
    
    with open(ruta_csv_agenda, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=encabezados)
        writer.writeheader()
        writer.writerows(agenda_medicos)


# Función para agregar un día y horario de atención de un medico.
def agregar_horario_medico(id_medico, dia_numero, hora_inicio, hora_fin):
    agenda = cargar_agenda_medicos()

    # Se verifica si el médico ya tiene ese horario agregado
    existe_horario = any(
        horario.get('id_medico') == str(id_medico) and
        horario.get('dia_numero') == str(dia_numero) and
        horario.get('hora_inicio') == hora_inicio and
        horario.get('hora_fin') == hora_fin
        for horario in agenda
    )

    if not existe_horario:

        nuevo_horario = {
            'id_medico': str(id_medico),
            'dia_numero': str(dia_numero),
            'hora_inicio': hora_inicio,
            'hora_fin': hora_fin,
            'fecha_actualizacion': datetime.now().strftime('%Y/%m/%d')
        }

        # Se agrega el nuevo horario a la lista existente
        agenda.append(nuevo_horario)
        
        exportar_csv_agenda(agenda)

        return True
    else:
        return False
    
    
# Función para modificar un dia y horario de atención de un medico.
def modificar_horario_medico(id_medico, dia_numero, hora_inicio_actual, hora_fin_actual, hora_inicio_nueva, hora_fin_nueva):
    agenda = cargar_agenda_medicos()

    # Primero se verifica si el médico trabaja eese día y tiene el horario que se quiere modificar.
    horario_a_modificar = next(
        (horario for horario in agenda
         if horario.get('id_medico') == str(id_medico) and
         horario.get('dia_numero') == str(dia_numero) and
         horario.get('hora_inicio') == hora_inicio_actual and
         horario.get('hora_fin') == hora_fin_actual), None
    )

    if horario_a_modificar:
        # Se modifica el horario existente
        horario_a_modificar['hora_inicio'] = hora_inicio_nueva
        horario_a_modificar['hora_fin'] = hora_fin_nueva
        horario_a_modificar['fecha_actualizacion'] = datetime.now().strftime('%Y/%m/%d')

        # Por ultimo se guarda
        exportar_csv_agenda(agenda)

        return True
    else:
        return False


# Función para eliminar los días de atención de un médico por su ID
def eliminar_dias_atencion_medico(id_medico):
    agenda = cargar_agenda_medicos()

    nueva_agenda = [horario for horario in agenda if horario.get('id_medico') != str(id_medico)]

    exportar_csv_agenda(nueva_agenda)

    return True if len(nueva_agenda) != len(agenda) else False

    
# Función que permite imprimir la agenda de manera ordenada.
def obtener_horarios_ordenados(): # Voy a llamar esta función cuando tenga que mostrar con GET todos los turnos.
    agenda = cargar_agenda_medicos()

    # Ordena la agenda por ID del médico y luego por num del dia.
    agenda_ordenada = sorted(agenda, key=lambda x: (int(x['id_medico']), int(x['dia_numero'])))

    return agenda_ordenada
