# 🍣 Ristorante Yami - Sistema di Gestione Ordini

<div align="center">
  <p><em>Un sistema moderno per la gestione degli ordini di sushi</em></p>
</div>

## 📋 Indice
- [Panoramica](#-panoramica)
- [Funzionalità](#-funzionalità)
- [Tecnologie Utilizzate](#-tecnologie-utilizzate)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Setup e Installazione](#-setup-e-installazione)
- [Utilizzo](#-utilizzo)
- [API e Endpoints](#-api-e-endpoints)
- [Database](#-database)

## 🎯 Panoramica
Yami è un sistema di gestione ordini per ristoranti di sushi che offre un'interfaccia intuitiva sia per i clienti che per lo staff della cucina. Il sistema permette ai clienti di effettuare ordini dal proprio tavolo e allo chef di gestire gli ordini in tempo reale.

## ✨ Funzionalità

### 👥 Lato Cliente
- **Login Tavolo**: Accesso sicuro tramite numero tavolo e password
- **Menu Interattivo**: Visualizzazione dei piatti con immagini e descrizioni
- **Gestione Ordini**: Possibilità di ordinare più piatti con quantità personalizzate
- **Monitoraggio Stati**: Tracciamento in tempo reale dello stato degli ordini

### 👨‍🍳 Lato Chef
- **Dashboard Chef**: Interfaccia dedicata per la gestione degli ordini
- **Gestione Stati**: Possibilità di:
  - Completare gli ordini
  - Segnare come consegnati
  - Sospendere ordini problematici
- **Visione d'Insieme**: Visualizzazione completa di tutti gli ordini attivi

## 🛠 Tecnologie Utilizzate
- **Backend**: Python Flask
- **Security**: Python Secrets
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (AJAX)
- **Template Engine**: Jinja2
- **Real-time Updates**: Polling System

## 📂 Struttura del Progetto
```
Risotrante Yami - Flask/
├── app.py                 # Application entry point
├── db_manager.py         # Database operations
├── Database/
│   └── db.sql           # Database schema
├── static/
│   ├── images/          # Product images
│   └── js/
│       └── orders.js    # Real-time order management
└── Templates/
    ├── login.html       # Customer login
    ├── loginChef.html   # Chef login
    ├── menu.html        # Menu display
    ├── cart.html        # Order tracking
    ├── orders.html      # Chef dashboard
    └── errPage.html     # Error handling
```

## 🚀 Setup e Installazione
1. Clone del repository:
```bash
git clone https://github.com/tuouser/ristorante-yami-flask.git
```

2. Creazione ambiente virtuale:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installazione dipendenze:
```bash
pip install -r requirements.txt
```

4. Avvio applicazione:
```bash
python app.py
```

## 💻 Utilizzo

### 🍽 Accesso Cliente
1. Accedi con il numero del tuo tavolo e la password fornita
2. Sfoglia il menu e seleziona i piatti desiderati
3. Specifica le quantità e conferma l'ordine
4. Monitora lo stato dei tuoi ordini nella sezione "I tuoi Ordini"

### 👨‍🍳 Accesso Chef
1. Accedi all'area chef tramite `/napafiniChef`
2. Usa le credenziali fornite (default: Soma/passw0rd)
3. Gestisci gli ordini in arrivo tramite i pulsanti di azione
4. Monitora tutti gli ordini attivi in tempo reale con aggiornamenti automatici ogni 5 secondi

## 🔄 Stati degli Ordini
- **🟡 Preparazione**: Ordine ricevuto e in lavorazione
- **🟢 Completato**: Pronto per la consegna
- **⚪ Consegnato**: Ordine servito al tavolo
- **🔴 Sospeso**: Ordine temporaneamente sospeso

## 🔄 Sistema di Aggiornamento in Tempo Reale
- **Polling Automatico**: Aggiornamento degli ordini ogni 5 secondi
- **Aggiornamenti Asincroni**: Nessun refresh della pagina richiesto
- **Gestione Errori**: Sistema robusto di gestione degli errori di rete
- **Efficienza**: Trasferimento solo dei dati necessari

## 💾 Database
Il sistema utilizza SQLite con le seguenti tabelle:
- `tavolo`: Gestione tavoli e credenziali
- `chef`: Autenticazione staff cucina
- `piatto`: Catalogo piatti disponibili
- `stato`: Stati possibili degli ordini
- `ordine`: Registro ordini con relazioni

## 🔐 Sicurezza
- Autenticazione separata per clienti e staff
- Gestione delle sessioni per accessi simultanei
- Validazione input per prevenire injection
- Gestione errori robusta

---
<div align="center">
  <p>Sviluppato con ❤️ per la ristorazione moderna</p>
</div>
