import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import db_manager
import secrets

# Create uploads folder if it doesn't exist
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.secret_key = secrets.token_hex(16)  # Generate a secure 32-character hex key

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db_manager.create_database()

@app.route('/')
def home():
    try:
        if 'tavolo_id' not in session:
            return redirect(url_for('login'))
        return redirect(url_for('menu'))
    except Exception as e:
        return render_template('errPage.html', error_message=str(e))

# Error routes
@app.route('/loginErr')
def loginErr():
    return render_template('errPage.html', error_message="Tavolo non trovato")

@app.route('/menuErr')
def menuErr():
    return render_template('errPage.html', error_message="Problema nel caricamento del menu")

@app.route('/ordineErr')
def ordineErr():
    return render_template('errPage.html', error_message="Errore nell'ordinazione")

@app.route('/adminAccessErr')
def adminAccessErr():
    return render_template('errPage.html', error_message="Accesso non autorizzato. È necessario essere autenticati come amministratore.")

@app.route('/chefAccessErr')
def chefAccessErr():
    return render_template('errPage.html', error_message="Accesso non autorizzato. È necessario essere autenticati come chef.")

@app.route('/adminRegistrationErr')
def adminRegistrationErr():
    return render_template('errPage.html', error_message="Errore nella registrazione dell'amministratore.")

@app.route('/chefRegistrationErr')
def chefRegistrationErr():
    return render_template('errPage.html', error_message="Errore nella registrazione del chef.")

@app.route('/plateAdditionErr')
def plateAdditionErr():
    return render_template('errPage.html', error_message="Errore nell'aggiunta del nuovo piatto.")

@app.route('/plateImageErr')
def plateImageErr():
    return render_template('errPage.html', error_message="Errore con l'immagine del piatto. Assicurarsi che sia un formato valido (PNG, JPG, JPEG, GIF).")

@app.route('/orderUpdateErr')
def orderUpdateErr():
    return render_template('errPage.html', error_message="Errore nell'aggiornamento dello stato dell'ordine.")

@app.route('/orderDeleteErr')
def orderDeleteErr():
    return render_template('errPage.html', error_message="Errore nell'eliminazione dell'ordine.")

# Add 404 error handler for non-existent routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errPage.html', error_message="Pagina non trovata. La rotta che hai richiesto non esiste."), 404

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
        return redirect(url_for('chefAccessErr'))
    
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
        return redirect(url_for('chefAccessErr'))
    
    try:
        ordine_id = request.form['ordine_id']
        action = request.form['action']
        
        if action == 'complete':
            db_manager.completa_ordine(ordine_id)
        elif action == 'deliver':
            db_manager.consegna_ordine(ordine_id)
        elif action == 'suspend':
            db_manager.sospendi_ordine(ordine_id)
        
        return redirect(url_for('orders'))
    except Exception as e:
        return redirect(url_for('orderUpdateErr'))

@app.route('/logout_chef')
def logout_chef():
    session.pop('chef_name', None)
    return redirect(url_for('chef_login'))

@app.route('/napafiniAdmin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        nome = request.form['nome']
        password = request.form['password']
        
        admin = db_manager.autentica_admin(nome, password)
        if admin:
            session['admin_name'] = admin['nome']
            session['admin_id'] = admin['id']
            return redirect(url_for('tables'))
        
        return redirect(url_for('loginErr'))
    
    return render_template('loginAdmin.html')

@app.route('/tables')
def tables():
    if 'admin_name' not in session:
        return redirect(url_for('adminAccessErr'))
    
    tavoli = db_manager.get_tavoli()
    return render_template('tables.html', tavoli=tavoli, admin_name=session['admin_name'])

@app.route('/admin_orders/<int:tavolo_id>')
def admin_orders(tavolo_id):
    if 'admin_name' not in session:
        return redirect(url_for('adminAccessErr'))
    
    try:
        tavolo = db_manager.get_tavolo_id(tavolo_id)
        ordini = db_manager.get_ordini_completi(tavolo_id)
        return render_template('orders.html', ordini=ordini, tavolo=tavolo, is_admin=True, admin_name=session['admin_name'])
    except Exception as e:
        return redirect(url_for('menuErr'))

@app.route('/delete_all_orders', methods=['POST'])
def delete_all_orders():
    if 'admin_name' not in session:
        return redirect(url_for('adminAccessErr'))
    
    try:
        db_manager.delete_all_orders()
        return redirect(url_for('tables'))
    except Exception as e:
        return redirect(url_for('orderDeleteErr'))

@app.route('/delete_tavolo_orders/<int:tavolo_id>', methods=['POST'])
def delete_tavolo_orders(tavolo_id):
    if 'admin_name' not in session:
        return redirect(url_for('adminAccessErr'))
    
    try:
        db_manager.delete_tavolo_orders(tavolo_id)
        return redirect(url_for('admin_orders', tavolo_id=tavolo_id))
    except Exception as e:
        return redirect(url_for('orderDeleteErr'))

@app.route('/delete_single_order/<int:ordine_id>/<int:tavolo_id>', methods=['POST'])
def delete_single_order(ordine_id, tavolo_id):
    if 'admin_name' not in session:
        return redirect(url_for('adminAccessErr'))
    
    try:
        db_manager.delete_single_order(ordine_id)
        return redirect(url_for('admin_orders', tavolo_id=tavolo_id))
    except Exception as e:
        return redirect(url_for('orderDeleteErr'))

@app.route('/logout_admin')
def logout_admin():
    session.pop('admin_name', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin_login'))

@app.route('/register_admin_page')
def register_admin_page():
    if 'admin_name' not in session:
        return redirect(url_for('adminAccessErr'))
    
    return render_template('registerAdmin.html')

@app.route('/register_admin', methods=['POST'])
def register_admin():
    if 'admin_name' not in session:
        return redirect(url_for('adminAccessErr'))
    
    nome = request.form['nome']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    # Check if passwords match
    if password != confirm_password:
        return render_template('registerAdmin.html', error="Le password non corrispondono.")
    
    # Check if admin name already exists
    admins = db_manager.get_all_admins()
    for admin in admins:
        if admin['nome'].lower() == nome.lower():
            return render_template('registerAdmin.html', error=f"Il nome '{nome}' è già in uso.")
    
    # Register new admin
    try:
        db_manager.create_admin(nome, password)
        return render_template('registerAdmin.html', success=f"L'admin '{nome}' è stato registrato con successo.")
    except Exception as e:
        return redirect(url_for('adminRegistrationErr'))

@app.route('/register_chef_page')
def register_chef_page():
    if 'admin_name' not in session:
        return redirect(url_for('adminAccessErr'))
    
    return render_template('registerChef.html')

@app.route('/register_chef', methods=['POST'])
def register_chef():
    if 'admin_name' not in session:
        return redirect(url_for('adminAccessErr'))
    
    nome = request.form['nome']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    # Check if passwords match
    if password != confirm_password:
        return render_template('registerChef.html', error="Le password non corrispondono.")
    
    # Check if chef name already exists
    chefs = db_manager.get_all_chefs()
    for chef in chefs:
        if chef['nome'].lower() == nome.lower():
            return render_template('registerChef.html', error=f"Il nome '{nome}' è già in uso.")
    
    # Register new chef
    try:
        db_manager.create_chef(nome, password)
        return render_template('registerChef.html', success=f"Il chef '{nome}' è stato registrato con successo.")
    except Exception as e:
        return redirect(url_for('chefRegistrationErr'))

@app.route('/add_plate_page')
def add_plate_page():
    if 'admin_name' not in session:
        return redirect(url_for('adminAccessErr'))
    
    return render_template('addPlate.html')

@app.route('/add_plate', methods=['POST'])
def add_plate():
    if 'admin_name' not in session:
        return redirect(url_for('adminAccessErr'))
    
    nome = request.form['nome']
    ingredienti = request.form['ingredienti']
    
    # Check if the post request has the file part
    if 'immagine' not in request.files:
        return render_template('addPlate.html', error="Nessun file caricato")
    
    file = request.files['immagine']
    
    # If user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        return render_template('addPlate.html', error="Nessun file selezionato")
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            
            # Create a unique filename to prevent overwriting
            base_name, extension = os.path.splitext(filename)
            unique_filename = f"{base_name}_{secrets.token_hex(8)}{extension}"
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Save relative path for database storage
            relative_path = f"uploads/{unique_filename}"
            
            db_manager.add_piatto(nome, ingredienti, relative_path)
            return render_template('addPlate.html', success=f"Il piatto '{nome}' è stato aggiunto con successo")
        except Exception as e:
            return redirect(url_for('plateAdditionErr'))
    else:
        return redirect(url_for('plateImageErr'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
