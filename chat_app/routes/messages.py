from flask import Blueprint

messages_bp = Blueprint("messages", __name__)

@messages_bp.route("/messages")
def get_messages():
    return {"message": "Endpoint de mensajes funcionando"}
