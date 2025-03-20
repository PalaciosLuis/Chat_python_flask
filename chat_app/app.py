from flask import Flask
from flask_socketio import SocketIO, send
from flask_login import LoginManager
from config import Config
from models import db
from routes.auth import auth_bp, login_manager
from routes.chat import chat_bp
from routes.messages import messages_bp
from dotenv import load_dotenv
from models.message import Message
import os
from flask_login import current_user

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar la base de datos y Flask-Login
db.init_app(app)
login_manager.init_app(app)

# Inicializar Flask-SocketIO
socketio = SocketIO(app)

# Registrar Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(chat_bp)
app.register_blueprint(messages_bp)

clients = {}

@socketio.on('connect')
def handle_connect():
    print("Usuario conectado")

@socketio.on('disconnect')
def handle_disconnect():
    print("Usuario desconectado")

@socketio.on('message')
def handle_message(msg):
    if current_user.is_authenticated:
        username = current_user.username  # Asegúrate de que tu modelo `User` tenga `username`
    else:
        username = "Anonimo"  # Usuario no autenticado

    new_message = Message(username=username, content=msg)
    db.session.add(new_message)
    db.session.commit()
    send(f"{username}: {msg}", broadcast=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Cargar configuración desde .env
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() in ['true', '1']

    socketio.run(app, host=host, port=port, debug=debug)

    
