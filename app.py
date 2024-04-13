# Trabajo Final Programacion II 2023  - Balot Luciano Nicolas 21430
# Desarrollo API REST para la gestión de turnos medicos

from flask import Flask

# Se cargan los Blueprint
from Controladores.ruta_agenda import agenda_bp
from Controladores.ruta_medicos import medicos_bp
from Controladores.ruta_pacientes import pacientes_bp
from Controladores.ruta_turnos import turnos_bp

app = Flask(__name__) # Se crea una instancia de la clase Flask.

# Se inician los modelos.

# Se registran los Blueprints en la aplicación.
app.register_blueprint(agenda_bp)
app.register_blueprint(turnos_bp)
app.register_blueprint(medicos_bp)
app.register_blueprint(pacientes_bp)

if __name__ == "__main__": # Inicio de la aplicación.
    
    app.run(debug=True)