import sqlite3
import json
import os
import mimetypes
from wsgiref.simple_server import make_server

# Función para sacar datos de la BD
def obtener_relatos_bd():
    conn = sqlite3.connect('cultura.db')
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, autor, tipo, region FROM relatos")
    filas = cursor.fetchall()
    conn.close()
    
    resultado = []
    for fila in filas:
        resultado.append({
            "titulo": fila[0],
            "autor": fila[1],
            "tipo": fila[2],
            "region": fila[3]
        })
    return resultado

# Aplicación WSGI
def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # API: Devuelve JSON
    if path == '/api/relatos' and method == 'GET':
        status = '200 OK'
        headers = [('Content-Type', 'application/json; charset=utf-8')]
        start_response(status, headers)
        return [json.dumps(obtener_relatos_bd()).encode('utf-8')]

    # ARCHIVOS ESTÁTICOS (CSS, JS, Imágenes en /static/)
    elif path.startswith('/static/'):
        file_path = path.lstrip('/') # Quita el '/' inicial
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            status = '200 OK'
            headers = [('Content-Type', mime_type or 'text/plain')]
            start_response(status, headers)
            with open(file_path, 'rb') as f:
                return [f.read()]
    
    # HTML (En la raíz)
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