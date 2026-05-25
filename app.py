from flask import Flask

from werkzeug.middleware.proxy_fix import ProxyFix

from config import (
    SECRET_KEY,
    SESSION_TIMEOUT
)


# =========================
# APP
# =========================

app = Flask(__name__)

app.secret_key = SECRET_KEY

app.permanent_session_lifetime = SESSION_TIMEOUT

app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_proto=1,
    x_host=1
)


# =========================
# IMPORTAR RUTAS
# =========================

from routes import *


# =========================
# MAIN
# =========================

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False
    )
