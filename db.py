import sqlite3 # libreria estandar de python para usar bases de datos sqlite

ruta_bd = 'logs_simple.db' # nombre del archivo de la base de datos (se crea si no existe)

def conectar_bd():
    return sqlite3.connect(ruta_bd) # abre una conexion a la base de datos (si no existe, la crea)

def crear_tabla_si_no_existe():
    # with abre la conexion y asegura de cerrar todo al salir
    with conectar_bd() as con:
        # ejecuta SQL: crea la tabla registros_log solo si no existe
        con.execute(
            '''
            CREATE TABLE IF NOT EXISTS registros_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                fecha_hora_evento TEXT NOT NULL,
                nombre_servicio TEXT NOT NULL,
                nivel_severidad TEXT NOT NULL,
                mensaje_evento TEXT NOT NULL,
                recibido_en TEXT NOT NULL
            )'''
        )
        # al salir del with se guardan los cambios y se cierra la conexion