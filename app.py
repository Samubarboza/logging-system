# servidor principal
from flask import Flask
from routes import bp_logs # importamos el blueprint con las rutas de logs
from db import crear_tabla_si_no_existe 

# creamos la app Flask (WSGI) 
app = Flask(__name__) # le decimos que este es el arhcivo principal

# registramos las rutas del blueprint en la app
app.register_blueprint(bp_logs) # agregamos las rutas de logs al servidor

# endpoint /salud -> responde si el servidor esta funcionando
@app.get('/check') # define la ruta get en /check
def check():
    return {'estado': 'ok'}, 200 # devuelve json con codigo 200 (exito)

# endpoint raiz / -> mensaje de bienvenida maas lista de endpoints
@app.get('/') # define la ruta GET en /
def raiz():
    return {
        'mensaje': 'servidor de logging activo', 
        'endpoints': ['/check', 'logs'] # lista de endpoints disponibles
    }, 200 # responde json con codigo 200 (exito)
    
# se ejecuta solo si este es el archivo principal
if __name__ == '__main__': # asegura que corra solo al ejecutar este archivo
    crear_tabla_si_no_existe() # crea la tabla de la bd
    app.run(host='127.0.0.1', port=8000, debug=True)