
from flask import Flask
from flask_login import LoginManager
from config import Config
from database import init_db
import sqlite3
import os

# =========================
# CREATE FLASK APP
# =========================

app = Flask(__name__)
app.config.from_object(Config)

# =========================
# LOGIN MANAGER
# =========================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


# =========================
# USER LOADER
# =========================

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password FROM users WHERE id=?",
        (user_id,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return User(*user)

    return None


# =========================
# INITIALIZE DATABASE
# =========================

init_db()


# =========================
# REGISTER BLUEPRINTS
# =========================

from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    from flask import Flask
from flask_login import LoginManager
from config import Config
from database import init_db
import sqlite3
import os

# =========================
# CREATE FLASK APP
# =========================

app = Flask(__name__)
app.config.from_object(Config)

# =========================
# LOGIN MANAGER
# =========================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


# =========================
# USER LOADER
# =========================

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password FROM users WHERE id=?",
        (user_id,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return User(*user)

    return None


# =========================
# INITIALIZE DATABASE
# =========================

init_db()


# =========================
# REGISTER BLUEPRINTS
# =========================

from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))