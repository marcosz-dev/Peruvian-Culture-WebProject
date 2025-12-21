import sqlite3

def init_db():
    conn = sqlite3.connect('cultura.db')
    cursor = conn.cursor()

    # Crear tabla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT,
            tipo TEXT,
            region TEXT
        )
    ''')

    # Datos iniciales
    relatos_iniciales = [
        ('Manco Cápac y Mama Ocllo', 'Tradición Oral', 'Mito', 'Sierra'),
        ('La leyenda del Muqui', 'Tradición Oral', 'Leyenda', 'Sierra'),
        ('El mito de Kon', 'Tradición Oral', 'Mito', 'Costa'),
        ('Los gallinazos sin plumas', 'Julio Ramón Ribeyro', 'Cuento', 'Costa'),
        ('El caballero Carmelo', 'Abraham Valdelomar', 'Cuento', 'Costa'),
        ('Calixto Garmendia', 'Ciro Alegría', 'Cuento', 'Sierra')
    ]

    cursor.executemany('INSERT INTO relatos (titulo, autor, tipo, region) VALUES (?, ?, ?, ?)', relatos_iniciales)
    conn.commit()
    conn.close()
    print("Base de datos 'cultura.db' creada con éxito.")

if __name__ == '__main__':
    init_db()