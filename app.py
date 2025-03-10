from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import db_manager
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a secure 32-character hex key

db_manager.create_database()

@app.route('/')
def home():
    try:
        if 'tavolo_id' not in session:
            return redirect(url_for('login'))
        return redirect(url_for('menu'))
    except Exception as e:
        return render_template('errPage.html', error_message=str(e))

@app.route('/loginErr')
def loginErr():
    return render_template('errPage.html', error_message="Tavolo non trovato")

@app.route('/menuErr')
def menuErr():
    return render_template('errPage.html', error_message="Problema nel caricamento del menu")

@app.route('/ordineErr')
def ordineErr():
    return render_template('errPage.html', error_message="Errore nell'ordinazione")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        numero_tavolo = request.form['tableNumber']
        password = request.form['password']
        
        print(f"Tentativo di login - Tavolo: {numero_tavolo}, Password: {password}")  # Debug log
        
        tavolo = db_manager.autentica_tavolo(numero_tavolo, password)
        if tavolo:
            print(f"Login riuscito per il tavolo ID: {tavolo['id']}")  # Debug log
            session['tavolo_id'] = tavolo['id']
            return redirect(url_for('home'))
        
        print("Login fallito - Tavolo non trovato")  # Debug log
        return redirect(url_for('loginErr'))
    
    return render_template('login.html')

@app.route('/menu')
def menu():
    try:
        if 'tavolo_id' not in session:
            return redirect(url_for('login'))
        
        tavolo_id = session['tavolo_id']
        tavolo = db_manager.get_tavolo_id(tavolo_id)
        piatti = db_manager.get_piatti()
        ordini = db_manager.get_tavolo_ordini(tavolo_id)
        
        if not piatti:
            return redirect(url_for('menuErr'))
        
        return render_template('menu.html', 
                             piatti=piatti, 
                             ordini=ordini, 
                             tavolo_numero=tavolo['numero_tavolo'])
    except Exception as e:
        return redirect(url_for('menuErr'))

@app.route('/cart')
def cart():
    try:
        if 'tavolo_id' not in session:
            return redirect(url_for('login'))
        
        tavolo_id = session['tavolo_id']
        ordini = db_manager.get_ordini_completi(tavolo_id)
        return render_template('cart.html', ordini=ordini)
    except Exception as e:
        return redirect(url_for('menuErr'))

@app.route('/ordina', methods=['POST'])
def ordina():
    if 'tavolo_id' not in session:
        return redirect(url_for('menuErr'))
    
    try:
        tavolo_id = session['tavolo_id']
        piatto_id = request.form['piatto_id']
        quantita = int(request.form['quantita'])
        
        if quantita < 1 or quantita > 10:
            return redirect(url_for('menuErr'))
        
        db_manager.crea_ordine(tavolo_id, piatto_id, quantita)
        return redirect(url_for('menu'))
    except Exception as e:
        return redirect(url_for('ordineErr'))

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))

@app.route('/napafiniChef', methods=['GET', 'POST'])
def chef_login():
    if request.method == 'POST':
        nome = request.form['nome']
        password = request.form['password']
        
        chef = db_manager.autentica_chef(nome, password)
        if chef:
            session['chef_name'] = chef['nome']
            return redirect(url_for('orders'))
        
        return redirect(url_for('loginErr'))
    
    return render_template('loginChef.html')

@app.route('/orders')
def orders():
    if 'chef_name' not in session:
        return redirect(url_for('chef_login'))
    
    ordini = db_manager.get_all_ordini()
    return render_template('orders.html', ordini=ordini, chef_name=session['chef_name'])

@app.route('/get_orders_data')
def get_orders_data():
    if 'chef_name' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    ordini = db_manager.get_all_ordini()
    return jsonify(ordini)

@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    if 'chef_name' not in session:
        return redirect(url_for('chef_login'))
    
    ordine_id = request.form['ordine_id']
    action = request.form['action']
    
    if action == 'complete':
        db_manager.completa_ordine(ordine_id)
    elif action == 'deliver':
        db_manager.consegna_ordine(ordine_id)
    elif action == 'suspend':
        db_manager.sospendi_ordine(ordine_id)
    
    return redirect(url_for('orders'))

@app.route('/logout_chef')
def logout_chef():
    session.pop('chef_name', None)
    return redirect(url_for('chef_login'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
