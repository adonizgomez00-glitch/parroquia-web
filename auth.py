from flask import (
    session,
    redirect,
    jsonify
)

from functools import wraps


# =========================
# USUARIOS
# =========================

USERS = {

    "admin": {
        "password": "pbkdf2:sha256:260000$cMBW90sDd4GKWBUb$3fb2638184a946d4dbfffb45d32b354710cca53728f5aba750c9b74f8a5c262b",
        "role": "admin"
    },

    "usuario": {
        "password": "pbkdf2:sha256:260000$IYT0o3nYQfKy5zUZ$b2c620bcbe5790442f0c64c82910e6de3996d8bc01f9a496d8d1ecc15ce2baa7",
        "role": "usuario"
    }

}


# =========================
# LOGIN REQUIRED
# =========================

def login_required(f):

    @wraps(f)

    def decorated(*args, **kwargs):

        if 'user' not in session:

            return redirect('/login')

        return f(*args, **kwargs)

    return decorated


# =========================
# ADMIN REQUIRED
# =========================

def admin_required(f):

    @wraps(f)

    def decorated(*args, **kwargs):

        if session.get('role') != 'admin':

            return jsonify({
                'error': 'Acceso denegado'
            }), 403

        return f(*args, **kwargs)

    return decorated
