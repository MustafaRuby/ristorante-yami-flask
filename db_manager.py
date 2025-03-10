import sqlite3

DATABASE = "yami.db"

sushi_items = [
    {"name": "Nigiri al Salmone", "ingredienti" : "Riso con fetta di salmone fresco", "nome_foto": "images/nigiri_salmone.jpg"},
    {"name": "Nigiri al Tonno", "ingredienti" : "Riso con fetta di tonno fresco", "nome_foto": "images/nigiri_tonno.jpg"},
    {"name": "Nigiri al Gambero", "ingredienti" : "Riso con gambero fresco", "nome_foto": "images/nigiri_gambero.jpg"},
    {"name": "Sashimi al Salmone", "ingredienti" : "Fette di salmone fresco", "nome_foto": "images/sashimi_salmone.jpg"},
    {"name": "Sashimi al Tonno", "ingredienti" : "Fette di tonno fresco", "nome_foto": "images/sashimi_tonno.jpg"},
    {"name": "Gunkan al Salmone", "ingredienti" : "Riso con salmone fresco e alga nori", "nome_foto": "images/gunkan_salmone.jpg"},
    {"name": "Gunkan al Tonno", "ingredienti" : "Riso con tonno fresco e alga nori", "nome_foto": "images/gunkan_tonno.jpg"},
    {"name": "Hoso al Salmone", "ingredienti" : "Riso con salmone fresco e avocado", "nome_foto": "images/sake_salmone.jpg"},
    {"name": "Hoso al Tonno", "ingredienti" : "Riso con tonno fresco e avocado", "nome_foto": "images/sake_tonno.jpg"},
    {"name": "Takito al Salmone", "ingredienti" : "Tortilla di mais con tartare di salmone, avocado, cetriolo, sesamo, salsa maionese piccante, salsa sriracha, salsa teriyaki", "nome_foto": "images/takito_salmone.jpg"},
]

stati = [
    {"name": "preparazione"},
    {"name": "completato"},
    {"name": "consegnato"},
    {"name": "sospeso"}
]

def DB_connect():
    connection = sqlite3.connect(DATABASE) # Connects to the database
    connection.row_factory = sqlite3.Row # Returns rows as dictionaries
    return connection

def create_database():
    with DB_connect() as connection, open('Database/db.sql', 'r') as file:
        connection.executescript(file.read())
        
        # Check if tables are empty
        cursor = connection.execute("SELECT COUNT(*) FROM tavolo")
        if cursor.fetchone()[0] == 0:
            # Insert default tables
            for x in range(1, 50):
                passw = "password" + str(x)
                connection.execute("INSERT INTO tavolo (numero_tavolo, password) VALUES (?, ?)", (x, passw))
            connection.commit()
        
        cursor = connection.execute("SELECT COUNT(*) FROM piatto")
        if cursor.fetchone()[0] == 0:
            for item in sushi_items:
                connection.execute("INSERT INTO piatto (nome, ingredienti, src_immagine) VALUES (?, ?, ?)", 
                                (item["name"], item["ingredienti"], item["nome_foto"]))
            connection.commit()
        
        cursor = connection.execute("SELECT COUNT(*) FROM stato")
        if cursor.fetchone()[0] == 0:
            for stato in stati:
                connection.execute("INSERT INTO stato(nome) VALUES (?)", (stato["name"],))
            connection.commit()
        
        cursor = connection.execute("SELECT COUNT(*) FROM chef")
        if cursor.fetchone()[0] == 0:
            connection.execute("INSERT INTO chef (nome, password) VALUES (?, ?)", 
                            ("Soma", "passw0rd"))
            connection.commit()

def autentica_tavolo(numero, password):
    with DB_connect() as connection:
        cursor = connection.execute("""
            SELECT * FROM tavolo 
            WHERE numero_tavolo = ? AND password = ?
        """, (numero, password))
        return cursor.fetchone()

def autentica_chef(nome, password):
    with DB_connect() as connection:
        cursor = connection.execute("""
            SELECT * FROM chef 
            WHERE nome = ? AND password = ?
        """, (nome, password))
        return cursor.fetchone()

def get_tavolo_numero(numero):
    with DB_connect() as connection:
        cursor = connection.execute("SELECT * FROM tavolo WHERE numero = ?", (numero,))
        return cursor.fetchone()

def get_tavolo_id(id):
    with DB_connect() as connection:
        cursor = connection.execute("SELECT * FROM tavolo WHERE id = ?", (id,))
        return cursor.fetchone()
    
def get_tavoli():
    with DB_connect() as connection:
        cursor = connection.execute("SELECT * FROM tavolo")
        return cursor.fetchall()

def get_piatti():
    with DB_connect() as connection:
        cursor = connection.execute("SELECT * FROM piatto")
        return cursor.fetchall()

def get_piatto_id(id):
    with DB_connect() as connection:
        cursor = connection.execute("SELECT * FROM piatto WHERE id = ?", (id,))
        return cursor.fetchone()

def get_tavolo_ordini(tavolo_id):
    with DB_connect() as connection:
        cursor = connection.execute("SELECT * FROM ordine WHERE ID_tavolo = ?", (tavolo_id,))
        return cursor.fetchall()
    
def crea_ordine(tavolo_id, piatto_id, quantita):
    with DB_connect() as connection:
        connection.execute("INSERT INTO ordine (ID_tavolo, ID_piatto, ID_stato, quantita) VALUES (?, ?, 1, ?)", 
                         (tavolo_id, piatto_id, quantita))
        connection.commit()

def completa_ordine(ordine_id):
    with DB_connect() as connection:
        connection.execute("UPDATE ordine SET ID_stato = 2 WHERE id = ?", (ordine_id,))
        connection.commit()

def consegna_ordine(ordine_id):
    with DB_connect() as connection:
        connection.execute("UPDATE ordine SET ID_stato = 3 WHERE id = ?", (ordine_id,))
        connection.commit()

def sospendi_ordine(ordine_id):
    with DB_connect() as connection:
        connection.execute("UPDATE ordine SET ID_stato = 4 WHERE id = ?", (ordine_id,))
        connection.commit()

def get_ordini_completi(tavolo_id):
    with DB_connect() as connection:
        cursor = connection.execute("""
            SELECT o.*, p.*, s.nome as stato_nome 
            FROM ordine o 
            JOIN piatto p ON o.ID_piatto = p.id 
            JOIN stato s ON o.ID_stato = s.id 
            WHERE o.ID_tavolo = ?
            ORDER BY o.id DESC
        """, (tavolo_id,))
        
        ordini = []
        for row in cursor.fetchall():
            ordini.append({
                'id': row['id'],
                'quantita': row['quantita'],
                'piatto': {
                    'nome': row['nome'],
                    'src_immagine': row['src_immagine']
                },
                'stato': {
                    'nome': row['stato_nome']
                }
            })
        return ordini

def get_all_ordini():
    with DB_connect() as connection:
        cursor = connection.execute("""
            SELECT o.*, p.nome as piatto_nome, p.src_immagine, t.numero_tavolo, s.nome as stato_nome 
            FROM ordine o 
            JOIN piatto p ON o.ID_piatto = p.id 
            JOIN tavolo t ON o.ID_tavolo = t.id 
            JOIN stato s ON o.ID_stato = s.id 
            ORDER BY o.id DESC
        """)
        
        ordini = []
        for row in cursor.fetchall():
            ordini.append({
                'id': row['id'],
                'quantita': row['quantita'],
                'tavolo_numero': row['numero_tavolo'],
                'piatto': {
                    'nome': row['piatto_nome'],
                    'immagine': row['src_immagine']
                },
                'stato': {
                    'nome': row['stato_nome']
                }
            })
        return ordini
