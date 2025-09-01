import requests # para las peticiones http
from datetime import datetime # para obtener fecha y hora actuales

# url del servidor - flask escucha los logs en el endpoint /logs
URL = 'http://127.0.0.1:8000/logs'
# token de autorizacion
TOKEN = 'abc'
# headers http qe acompañan la peticion - Content-Type dice que el cuerpo es json - Authorization  lleva el token en el formato esperado
headers = {'Content-Type': 'application/json', 'Authorization': f'Token {TOKEN}'}

# cuerpo del log que vamos a enviar al servidor
cuerpo = {
    'timestamp': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),  # fecha/hora actual en UTC, formato ISO corto
    'service': 'servicio_pagos',  # nombre del servicio que genera el log
    'severity': 'ERROR',  # nivel de severidad del log
    'message': 'tarjeta rechazada'  # mensaje descriptivo del evento
}

# hacemos un post al servidor
r = requests.post(URL, json=cuerpo, headers=headers, timeout=10)

print(r.status_code, r.text)