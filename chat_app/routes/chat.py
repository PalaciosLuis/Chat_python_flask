from flask import render_template
from flask_login import login_required, current_user
from . import chat_bp

@chat_bp.route('/')
@login_required
def index():
    return render_template('chat.html', username=current_user.username)
