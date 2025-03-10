CREATE TABLE IF NOT EXISTS tavolo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_tavolo INTEGER NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chef(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS piatto(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    ingredienti TEXT NOT NULL,
    src_immagine TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stato(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL --Preparazione, completato, consegnato, sospeso
);

CREATE TABLE IF NOT EXISTS ordine(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_tavolo INTEGER NOT NULL,
    ID_piatto INTEGER NOT NULL,
    ID_stato INTEGER NOT NULL,
    quantita INTEGER NOT NULL,
    FOREIGN KEY (ID_tavolo) REFERENCES tavolo(id),
    FOREIGN KEY (ID_piatto) REFERENCES piatto(id),
    FOREIGN KEY (ID_stato) REFERENCES stato(id)
);


