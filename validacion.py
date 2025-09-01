from datetime import datetime

# valida que el texto tenga formato ISO corto (YYYY-MM-DDTHH:MM:SS)
def parsear_iso_corto(texto: str) -> str:
    datetime.strptime(texto, "%Y-%m-%dT%H:%M:%S")
    return texto

# valida un log recibido y devuelve un diccionario normalizado
def validar_log(log_entrada: dict) -> dict:
    # verificar que estén todos los campos obligatorios
    for campo in ('timestamp', 'service', 'severity', 'message'):
        if campo not in log_entrada:
            raise ValueError(f'Falta el campo {campo}')
    
    # limpiar y validar cada valor
    fecha_evento = parsear_iso_corto(str(log_entrada['timestamp']).strip())
    nombre_servicio = str(log_entrada['service']).strip()
    nivel_severidad = str(log_entrada['severity']).upper().strip()
    mensaje_evento = str(log_entrada['message']).strip()
    
# valida que servicio y mensaje no estén vacíos, normaliza WARNING a WARN y acepta solo severidades válidas
    if not nombre_servicio or not mensaje_evento:
        raise ValueError('service/message vacios')
    if nivel_severidad == 'WARNING': nivel_severidad = 'WARN'
    if nivel_severidad not in {'INFO', 'DEBUG', 'ERROR', 'WARN'}:
        raise ValueError('severity invalido (use INFO/DEBUG/ERROR/WARN)')
    
    # devolver log listo para guardar en la BD
    return {
        'fecha_hora_evento': fecha_evento,
        'nombre_servicio': nombre_servicio,
        'nivel_severidad': nivel_severidad,
        'mensaje_evento': mensaje_evento,
        'recibido_en': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
    }
