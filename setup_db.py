import mysql.connector

def init_db():
    print("Conectando a MySQL...")
    
    # Conexión inicial al servidor (sin base de datos específica)
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin123" 
        )
        cursor = conn.cursor()

        # Crear la Base de Datos (si no existe)
        cursor.execute("CREATE DATABASE IF NOT EXISTS cultura_db")
        print("Base de datos 'cultura_db' verificada.")

        # Usar la Base de Datos
        cursor.execute("USE cultura_db")

        # Crear tabla RELATOS 
        # INT AUTO_INCREMENT en lugar de INTEGER AUTOINCREMENT
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relatos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                autor VARCHAR(255),
                tipo VARCHAR(50),
                region VARCHAR(50),
                contenido TEXT
            )
        ''')

        # 5. Crear tabla MENSAJES 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                asunto VARCHAR(255),
                mensaje TEXT
            )
        ''')

        # Insertar datos (Solo si la tabla está vacía para no duplicar)
        cursor.execute("SELECT COUNT(*) FROM relatos")
        count = cursor.fetchone()[0]
        
        if count == 0:
            relatos_iniciales = [
                ('Manco Cápac y Mama Ocllo', 'Tradición Oral', 'Mito', 'Sierra', 'Cuentan que el dios Sol, Inti, apiadado de la barbarie en que vivían los hombres, envió a sus hijos Manco Cápac y Mama Ocllo para civilizarlos. Salieron de las espumas del Lago Titicaca llevando una vara de oro. El dios Sol les había ordenado que se establecieran allí donde la vara se hundiera con facilidad. Tras mucho andar hacia el norte, llegaron al cerro Huanacaure, donde la vara se hundió en la tierra. Allí fundaron la ciudad del Cusco, el "Ombligo del Mundo", y enseñaron a los hombres la agricultura y a las mujeres el tejido.'),
                ('La leyenda del Muqui', 'Tradición Oral', 'Leyenda', 'Sierra', 'El Muqui es un duende minero que habita en el interior de las minas de la sierra peruana. Es pequeño, de piel pálida, y a menudo lleva un casco de oro y una lámpara. Se dice que es el verdadero dueño de los minerales. Los mineros le tienen mucho respeto y le dejan ofrendas de coca, alcohol y cigarros en los rincones oscuros de los socavones para que les permita encontrar buenas vetas de mineral y para evitar accidentes.'),
                ('El mito de Kon', 'Tradición Oral', 'Mito', 'Costa', 'Kon era un dios antiguo de la costa peruana, representado como un ser volador, sin huesos y ligero como una pluma. Él aplanó las tierras y creó llanuras fértiles. Sin embargo, al enojarse con los humanos porque no le rendían el culto adecuado, decidió castigarlos: transformó la tierra fértil en extensos desiertos de arena seca.'),
                ('Los gallinazos sin plumas', 'Julio Ramón Ribeyro', 'Cuento', 'Costa', 'A las seis de la mañana la ciudad se levanta de puntillas... Efraín y Enrique eran dos niños explotados por su abuelo, el viejo don Santos. Todos los días debían ir al muladar a buscar comida para el cerdo Pascual. Es una cruda historia sobre la marginalidad urbana en Lima.'),
                ('El caballero Carmelo', 'Abraham Valdelomar', 'Cuento', 'Costa', 'El Caballero Carmelo era un gallo de pelea, esbelto y orgulloso, que llegó a la casa de Pisco como un regalo. Tuvo que pelear contra el "Ajiseco" para defender el honor familiar. Ganó, pero murió poco después a causa de las heridas.'),
                ('Calixto Garmendia', 'Ciro Alegría', 'Cuento', 'Sierra', 'Déjame contarte. Yo nací arriba... Calixto Garmendia era un indio que luchó toda su vida contra la injusticia y el despojo de sus tierras. Nunca fue escuchado por las autoridades, pero dejó en su hijo la semilla de la protesta.')
            ]
            
            # MySQL usa %s en lugar de ? para los placeholders
            sql = "INSERT INTO relatos (titulo, autor, tipo, region, contenido) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(sql, relatos_iniciales)
            conn.commit()
            print("Datos iniciales insertados correctamente.")
        else:
            print("La base de datos ya tenía datos. No se hicieron cambios.")

        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("Asegúrate de que MySQL esté encendido (XAMPP/Start) y que el usuario sea correcto.")

if __name__ == '__main__':
    init_db()