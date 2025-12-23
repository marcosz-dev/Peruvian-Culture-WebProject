import json
import os
import mimetypes
from wsgiref.simple_server import make_server
import mysql.connector # conector de MySQL

# --- CONFIGURACIÓN DE CONEXIÓN ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin123", 
        database="cultura_db"
    )

# --- FUNCIONES DE BASE DE DATOS ---
def obtener_relatos_bd():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT titulo, autor, tipo, region, contenido FROM relatos")
        filas = cursor.fetchall()
        conn.close()
        
        # Convertir las tuplas a diccionarios
        return [{"titulo":f[0], "autor":f[1], "tipo":f[2], "region":f[3], "contenido":f[4]} for f in filas]
    except Exception as e:
        print(f"Error BD: {e}")
        return []

def guardar_mensaje(nombre, email, asunto, mensaje):
    conn = get_db_connection()
    cursor = conn.cursor()
    # MySQL usa %s como placeholder
    sql = "INSERT INTO mensajes (nombre, email, asunto, mensaje) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (nombre, email, asunto, mensaje))
    conn.commit()
    conn.close()

def obtener_mensajes_bd():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, asunto, mensaje FROM mensajes")
    filas = cursor.fetchall()
    conn.close()
    return [{"id":f[0], "nombre":f[1], "email":f[2], "asunto":f[3], "mensaje":f[4]} for f in filas]

# --- APLICACIÓN WSGI ---
def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # API: OBTENER RELATOS (GET)
    if path == '/api/relatos' and method == 'GET':
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [json.dumps(obtener_relatos_bd()).encode('utf-8')]

    # API: GUARDAR CONTACTO (POST)
    elif path == '/api/contacto' and method == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length).decode('utf-8')
            datos = json.loads(body)
            
            guardar_mensaje(datos['nombre'], datos['email'], datos['asunto'], datos['mensaje'])
            
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps({"status": "ok", "mensaje": "Recibido"}).encode('utf-8')]
        except Exception as e:
            print(f"Error POST: {e}")
            start_response('500 Error', [('Content-Type', 'text/plain')])
            return [str(e).encode('utf-8')]

    # API: VER MENSAJES (GET - Para el admin)
    elif path == '/api/mensajes' and method == 'GET':
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [json.dumps(obtener_mensajes_bd()).encode('utf-8')]

    # ARCHIVOS ESTÁTICOS
    elif path.startswith('/static/'):
        file_path = path.lstrip('/') 
        if os.path.exists(file_path) and os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            start_response('200 OK', [('Content-Type', mime_type or 'text/plain')])
            with open(file_path, 'rb') as f: return [f.read()]
    
    # HTML
    else:
        filename = 'index.html' if path == '/' else path.lstrip('/')
        if os.path.exists(filename) and os.path.isfile(filename) and filename.endswith('.html'):
            start_response('200 OK', [('Content-Type', 'text/html')])
            with open(filename, 'rb') as f: return [f.read()]
        else:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b"Error 404"]

if __name__ == '__main__':
    print("Servidor corriendo en http://localhost:8000 ...")
    httpd = make_server('', 8000, application)
    httpd.serve_forever()