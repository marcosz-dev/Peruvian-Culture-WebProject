import sqlite3
import json
import os
import mimetypes
from wsgiref.simple_server import make_server

# --- LÓGICA DE BASE DE DATOS ---
def obtener_relatos_bd():
    conn = sqlite3.connect('cultura.db')
    cursor = conn.cursor()
    
    # ¡AQUÍ ESTABA EL PROBLEMA! Faltaba pedir 'contenido' en esta lista
    cursor.execute("SELECT titulo, autor, tipo, region, contenido FROM relatos")
    filas = cursor.fetchall()
    conn.close()
    
    resultado = []
    for fila in filas:
        resultado.append({
            "titulo": fila[0],
            "autor": fila[1],
            "tipo": fila[2],
            "region": fila[3],
            "contenido": fila[4]  # <-- Y aquí lo empaquetamos para enviarlo
        })
    return resultado

# --- APLICACIÓN WSGI ---
def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # 1. RUTA API: Datos JSON
    if path == '/api/relatos' and method == 'GET':
        status = '200 OK'
        headers = [('Content-Type', 'application/json; charset=utf-8')]
        start_response(status, headers)
        datos = obtener_relatos_bd()
        return [json.dumps(datos).encode('utf-8')]

    # 2. RUTAS ESTÁTICAS (CSS, JS, Imágenes en /static/)
    elif path.startswith('/static/'):
        file_path = path.lstrip('/') 
        if os.path.exists(file_path) and os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            status = '200 OK'
            headers = [('Content-Type', mime_type or 'text/plain')]
            start_response(status, headers)
            with open(file_path, 'rb') as f:
                return [f.read()]
    
    # 3. RUTAS DE PÁGINAS HTML (En la raíz)
    else:
        filename = 'index.html' if path == '/' else path.lstrip('/')
        if os.path.exists(filename) and os.path.isfile(filename) and filename.endswith('.html'):
            status = '200 OK'
            headers = [('Content-Type', 'text/html; charset=utf-8')]
            start_response(status, headers)
            with open(filename, 'rb') as f:
                return [f.read()]
        else:
            status = '404 Not Found'
            headers = [('Content-Type', 'text/plain; charset=utf-8')]
            start_response(status, headers)
            return [b"Error 404: Archivo no encontrado."]

    return [b"Error 404"]

if __name__ == '__main__':
    port = 8000
    print(f"Servidor corriendo en http://localhost:{port} ...")
    httpd = make_server('', port, application)
    httpd.serve_forever()