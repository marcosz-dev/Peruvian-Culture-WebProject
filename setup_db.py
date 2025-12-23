import sqlite3
import os

def init_db():
    conn = sqlite3.connect('cultura.db')
    cursor = conn.cursor()

    # Crea la tabla relatos
    cursor.execute('''
        CREATE TABLE relatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT,
            tipo TEXT,    
            region TEXT,  
            contenido TEXT 
        )
    ''')

    # Crea tabla de mensajes de contacto
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            asunto TEXT,
            mensaje TEXT
        )
    ''')

    # Datos Iniciales
    relatos_iniciales = [
        (
            'Manco Cápac y Mama Ocllo', 
            'Tradición Oral', 
            'Mito', 
            'Sierra',
            'Cuentan que el dios Sol, Inti, apiadado de la barbarie en que vivían los hombres, envió a sus hijos Manco Cápac y Mama Ocllo para civilizarlos. Salieron de las espumas del Lago Titicaca llevando una vara de oro. El dios Sol les había ordenado que se establecieran allí donde la vara se hundiera con facilidad. Tras mucho andar hacia el norte, llegaron al cerro Huanacaure, donde la vara se hundió en la tierra. Allí fundaron la ciudad del Cusco, el "Ombligo del Mundo", y enseñaron a los hombres la agricultura y a las mujeres el tejido.'
        ),
        (
            'La leyenda del Muqui', 
            'Tradición Oral', 
            'Leyenda', 
            'Sierra',
            'El Muqui es un duende minero que habita en el interior de las minas de la sierra peruana. Es pequeño, de piel pálida, y a menudo lleva un casco de oro y una lámpara. Se dice que es el verdadero dueño de los minerales. Los mineros le tienen mucho respeto y le dejan ofrendas de coca, alcohol y cigarros en los rincones oscuros de los socavones para que les permita encontrar buenas vetas de mineral y para evitar accidentes. Si el Muqui se enoja o se siente ignorado, puede provocar derrumbes o perder a los mineros en laberintos subterráneos.'
        ),
        (
            'El mito de Kon', 
            'Tradición Oral', 
            'Mito', 
            'Costa',
            'Kon era un dios antiguo de la costa peruana, representado como un ser volador, sin huesos y ligero como una pluma. Él aplanó las tierras y creó llanuras fértiles. Sin embargo, al enojarse con los humanos porque no le rendían el culto adecuado, decidió castigarlos: transformó la tierra fértil en extensos desiertos de arena seca y dejó solo unos pocos ríos para que sobrevivieran con mucho esfuerzo. Fue finalmente desplazado por el dios Pachacámac.'
        ),
        (
            'Los gallinazos sin plumas', 
            'Julio Ramón Ribeyro', 
            'Cuento', 
            'Costa',
            'A las seis de la mañana la ciudad se levanta de puntillas... Efraín y Enrique eran dos niños explotados por su abuelo, el viejo don Santos, un hombre avaro y cruel que tenía un cerdo llamado Pascual. Todos los días, los niños debían ir al muladar (basural) a buscar comida para engordar al cerdo. El ambiente era de miseria y opresión. Un día, Efraín se cortó el pie con un vidrio, pero el abuelo no le permitió descansar. Al final, en una lucha desesperada por sobrevivir y protegerse mutuamente, los niños huyen mientras el abuelo sufre un destino fatal en el chiquero. Es una cruda historia sobre la marginalidad urbana en Lima.'
        ),
        (
            'El caballero Carmelo', 
            'Abraham Valdelomar', 
            'Cuento', 
            'Costa',
            'El Caballero Carmelo era un gallo de pelea, esbelto y orgulloso, que llegó a la casa de Pisco como un regalo para el padre. Se convirtió en la mascota querida de la familia, envejeciendo tranquilo. Sin embargo, un día el honor de la familia fue puesto en juego y el Carmelo, ya viejo, tuvo que volver a pelear contra el "Ajiseco", un gallo joven y fuerte. En una batalla épica y sangrienta, el Carmelo sacó fuerzas de flaqueza y logró vencer, salvando el orgullo familiar. Lamentablemente, murió poco después a causa de las heridas, dejando un gran vacío en el corazón de los niños de la casa.'
        ),
        (
            'Calixto Garmendia', 
            'Ciro Alegría', 
            'Cuento', 
            'Sierra',
            'Déjame contarte. Yo nací arriba, en un pueblito de los Andes... Calixto Garmendia era un indio carpintero y dueño de tierras que luchó toda su vida contra la injusticia. Las autoridades y los gamonales le arrebataron sus tierras con engaños legales. Calixto no se rindió: escribió cartas al gobierno, reclamó justicia y denunció los abusos, pero nunca fue escuchado. Murió pobre, pero con la dignidad intacta, dejando en su hijo la semilla de la protesta y la memoria de una lucha desigual contra el sistema opresor.'
        )
    ]

    cursor.executemany('INSERT INTO relatos (titulo, autor, tipo, region, contenido) VALUES (?, ?, ?, ?, ?)', relatos_iniciales)
    
    conn.commit()
    conn.close()
    print("Base de datos actualizada")

if __name__ == '__main__':
    init_db()