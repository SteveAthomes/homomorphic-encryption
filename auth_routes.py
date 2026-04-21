from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from extensions import bcrypt
from models.user import User
import sqlite3
from config import Config

auth_bp = Blueprint("auth", __name__)

# REGISTER
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

        try:
            conn = sqlite3.connect(Config.DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()

            return redirect(url_for("auth.login"))

        except sqlite3.IntegrityError:
            flash("Username already exists.")
            return redirect(url_for("auth.register"))

    return render_template("register.html")


# LOGIN
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(Config.DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[1], password):
            login_user(User(user[0]))
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid credentials.")

    return render_template("login.html")


# LOGOUT
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))