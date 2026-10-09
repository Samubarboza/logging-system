# Logging Distribuido

## ¿Qué es esto?

Un servidor central de logging hecho con Flask.
Varios servicios (simulados) le mandan sus errores y mensajes en formato JSON, y este servidor los guarda en una base SQLite.
En resumen:

* Los servicios tiran logs →
* El servidor los recibe, valida y guarda →
* Después podés consultarlos con filtros por fecha.

## Requisitos

* Python 3.10+
* Librerías:

  ```bash
  pip install flask
  ```


## Estructura

``
.
├── app.py            # servidor principal
├── auth.py           # validación de tokens
├── db.py             # conexión y tabla SQLite
├── routes.py         # endpoints /logs
├── validacion.py     # funciones para validar logs
└── logs_simple.db    # base de datos (se genera sola)
``

## Cómo correrlo

1. Clonar el repo y entrar a la carpeta.
2. Crear entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ``
3. Instalar Flask:

   ```bash
   pip install flask
   ``
4. Correr el servidor:

   ```bash
   python app.py
   ```

Servidor disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Endpoints

### GET /check

Chequeo de vida.

```json
{"estado": "ok"}
```

### POST /logs

Envío de uno o varios logs en JSON.

* Header obligatorio:

  ``
  Authorization: Token abc
  ``
* Ejemplo:

  ```bash
  curl -X POST http://127.0.0.1:8000/logs \
    -H "Content-Type: application/json" \
    -H "Authorization: Token abc" \
    -d '{"timestamp":"2025-09-01T10:00:00","service":"api_usuarios","severity":"INFO","message":"todo bien"}'
  ```

Respuesta:

```json
{"registros_guardados": 1}
```

### GET /logs

Consulta de logs guardados, con filtros opcionales:

* `timestamp_start` / `timestamp_end` → fecha del evento
* `received_at_start` / `received_at_end` → fecha de recepción en el servidor
* `cantidad_maxima_de_logs` → límite (default 50, máximo 500)
* `cantidad_de_logs_a_saltar` → offset (default 0)

Ejemplo:

```bash
curl "http://127.0.0.1:8000/logs?timestamp_start=2025-09-01T00:00:00&timestamp_end=2025-09-01T23:59:59"
```

Respuesta:

```json
{
  "cantidad_resultados": 2,
  "items": [
    {
      "id": 1,
      "fecha_hora_evento": "2025-09-01T10:00:00",
      "nombre_servicio": "api_usuarios",
      "nivel_severidad": "INFO",
      "mensaje_evento": "todo bien",
      "recibido_en": "2025-09-01T13:00:00"
    }
  ]
}
```

## Autenticación

* Tokens válidos están en `auth.py`.
* Formato esperado:

  ``
  Authorization: Token <tu_token>
  ``
* Si no es válido:

  ```json
  {"error": "Quien sos bro?"}
  ```

## Base de datos

* SQLite (`logs_simple.db`)
* Tabla `registros_log`:

  * `id`
  * `fecha_hora_evento`
  * `nombre_servicio`
  * `nivel_severidad`
  * `mensaje_evento`
  * `recibido_en`

## Bonus (para futuro)

* Endpoint `/stats` con métricas
* Limpieza automática de logs viejos
* JWT en lugar de tokens fijos
