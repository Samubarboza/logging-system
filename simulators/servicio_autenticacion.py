import requests # libreria para hacer peticiones HTTP
from datetime import datetime # para manejar fechas y horas

URL = 'http://127.0.0.1:8000/logs'  # dirección del servidor Flask (endpoint /logs)
TOKEN = 'xyz789'  # token válido para autenticar la petición
HEADERS = {'Content-Type': 'application/json', 'Authorization': f'Token {TOKEN}'}
# cabeceras: tipo de contenido json + el toquen de autorizacion

cuerpo = { # datos que vamos a mandar al servidor como json
    "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),  # fecha/hora actual UTC en formato ISO corto
    "service": "servicio_autenticacion",  # nombre del servicio que envía el log
    "severity": "INFO",  # nivel de severidad (INFO, DEBUG, WARN, ERROR)
    "message": "prueba de autenticación"  # mensaje que describe el evento
    }

r = requests.post(URL, json=cuerpo, headers=HEADERS, timeout=10)
# hace una peticion POST a logs, manda el cuerpo como json con headers y espera maximo 10 seg

print(r.status_code, r.text)
# imprime el codigo de respuesta http y el contenido devuelto