from flask import Flask, render_template, request, send_file, session, redirect, url_for
from flask_session import Session
import os
import requests

app = Flask(__name__)

# Configuración de la sesión
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'secret'  # Cambia esto a una clave más segura en producción
Session(app)

# Predefined user data
usuarios = {
    "yery": {
        "email": "marcovnx@gmail.com",
        "password": "witherstealer"
    }
}

@app.route('/')
def index():
    username = os.getlogin()
    try:
        ip_address = requests.get('https://api.ipify.org').text
    except requests.RequestException:
        ip_address = "Unable to obtain IP"

    with open('info.txt', 'w') as f:
        f.write(f"Username: {username}\n")
        f.write(f"Ip: {ip_address}\n")

    return render_template('index.html', logged_in=session.get('logged_in', False), username=session.get('username', 'Guest'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        if nombre in usuarios:
            return f"User '{nombre}' already exists with email {usuarios[nombre]['email']}."
        else:
            usuarios[nombre] = {
                "email": email,
                "password": password
            }
            return f"User registered: {nombre}, email: {email}"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        
        if nombre in usuarios and usuarios[nombre]['password'] == password:
            session['logged_in'] = True
            session['username'] = nombre
            return redirect(url_for('dashboard'))  # Redirigir al dashboard
        else:
            return "Incorrect username or password."
    return render_template('login.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Redirigir si no está logueado

    if request.method == 'POST':
        token = request.form['token']
        server_id = request.form['server_id']
        filename = request.form['filename']
        icon = request.files.get('icon')

        # Handle token, server ID, and icon logic here

        file_path = f"{filename}.exe"
        with open(file_path, 'wb') as f:
            f.write(b"This is a sample .exe file.")

        if icon:
            icon_path = f'uploads/{icon.filename}'
            icon.save(icon_path)

        return send_file(file_path, as_attachment=True)

    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()  # Elimina la sesión
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
