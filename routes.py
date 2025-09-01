from flask import Blueprint, request, jsonify
from auth import es_token_valido 
from validacion import validar_log, parsear_iso_corto
from db import conectar_bd

# crea un grupo de rutas llamado bp_logs y le da a Flask el contexto del módulo para ubicar de dónde vienen
bp_logs = Blueprint('bp_logs', __name__)

# procesa la petición POST: valida token, valida los logs recibidos y los guarda en la base
@bp_logs.route('/logs', methods=['POST'])
def crear_logs():
    if not es_token_valido(request.headers.get('Authorization')):
        return jsonify({'error': 'Quien sos bro?'}), 401 # no autorizado
    
    # intenta leer el cuerpo como JSON; con silent=True no rompe y devuelve None si no es JSON
    data = request.get_json(silent=True)
    if data is None: return jsonify({'error': 'JSON invalido'}), 400 # si no hay json, error
    logs_recibidos = data if isinstance(data, list) else [data]
    
    try:
        logs_validados = [validar_log(x) for x in logs_recibidos]
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    # abre conexión a la base de datos, inserta todos los logs validados y devuelve cuántos se guardaron
    with conectar_bd() as con:
        con.executemany(
            '''
            INSERT INTO registros_log
            (fecha_hora_evento, nombre_servicio, nivel_severidad, mensaje_evento, recibido_en)
            VALUES (:fecha_hora_evento, :nombre_servicio, :nivel_severidad, :mensaje_evento, :recibido_en)
            ''', logs_validados
        )
        return jsonify({'registros_guardados': len(logs_validados)}), 200 # (exito)
    
    # procesa la petición GET: lee filtros de fechas y límites desde la URL, arma la consulta SQL
@bp_logs.route('/logs', methods=['GET']) 
def listar_logs():
    # fechas de los eventos - de cuando ocurrio el log
    fecha_evento_desde = request.args.get('fecha_hora_evento_desde') or request.args.get('timestamp_start')
    fecha_evento_hasta = request.args.get('fecha_hora_evento_hasta') or request.args.get('timestamp_end')

    # fechas de los ventos - de cuando el servidor recibio el log
    fecha_recibido_desde = request.args.get('recibido_en_desde') or request.args.get('received_at_start')
    fecha_recibido_hasta = request.args.get('recibido_en_hasta') or request.args.get('received_at_end')

    
    try:
        cantidad_maxima_de_logs = min(int(request.args.get('cantidad_maxima_de_logs', '50')), 500)
        cantidad_de_logs_a_saltar = int(request.args.get('cantidad_de_logs_a_saltar', '0'))
    except ValueError:
        return jsonify({'error': 'limite/desplazamiento deben ser enteros'}), 400 # 400 datos invalidos
    
    lista_condiciones_sql, valores_condiciones = [], {}

    # arma filtros de fechas para la consulta
    def agregar_condicion_de_fecha(columna_sql, fecha_desde, fecha_hasta):
        if fecha_desde:
            parsear_iso_corto(fecha_desde)
            lista_condiciones_sql.append(f'{columna_sql} >= :{columna_sql}_desde')
            valores_condiciones[f'{columna_sql}_desde'] = fecha_desde

        if fecha_hasta:
            parsear_iso_corto(fecha_hasta)
            lista_condiciones_sql.append(f'{columna_sql} <= :{columna_sql}_hasta')
            valores_condiciones[f'{columna_sql}_hasta'] = fecha_hasta
            
        # aplica filtros de fecha y devuelve error 400 si alguna es inválida
    try:
        agregar_condicion_de_fecha('fecha_hora_evento', fecha_evento_desde, fecha_evento_hasta)
        agregar_condicion_de_fecha('recibido_en', fecha_recibido_desde, fecha_recibido_hasta)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    # arma el where para poder hacer la consulta
    where_sql = ('WHERE ' + ' AND '.join(lista_condiciones_sql)) if lista_condiciones_sql else ''
    
    # consulta con filtros (si hay), orden por mas nuevo primero y paginacion
    sql = f'''
    SELECT id, fecha_hora_evento, nombre_servicio, nivel_severidad, mensaje_evento, recibido_en
    FROM registros_log
    {where_sql}
    ORDER BY id DESC
    LIMIT :cantidad_maxima_de_logs OFFSET :cantidad_de_logs_a_saltar'''
    
    # guarda cantidad_maxima_de_logs y cantidad_de_logs_a_saltar para usarlos en el SQL
    valores_condiciones.update({'cantidad_maxima_de_logs':cantidad_maxima_de_logs, 'cantidad_de_logs_a_saltar': cantidad_de_logs_a_saltar})
    
# consulta la BD con filtros, convierte los resultados a JSON y los devuelve
    with conectar_bd() as con: 
        resultados_sql = con.execute(sql, valores_condiciones).fetchall()
        logs_encontrados = [{'id': r[0], 'fecha_hora_evento': r[1], 'nombre_servicio': r[2], 'nivel_severidad': r[3], 'mensaje_evento': r[4], 'recibido_en': r[5]} for r in resultados_sql]
        
        return jsonify({'cantidad_resultados': len(logs_encontrados), 'items': logs_encontrados}),200 # convertimos a json y devolvemos estado de exito