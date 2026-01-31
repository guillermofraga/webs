from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario, db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Ruta de login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
            user = db.usuarios.find_one({"email": email})

            if user and check_password_hash(user["password"], password):
                usuario_obj = Usuario(user["_id"], user["email"])
                login_user(usuario_obj)
                return redirect(url_for("index"))
            else:
                return render_template("auth/login.html", error="Credenciales incorrectas")
        except Exception as e:
            return render_template("auth/login.html", error="No se pudo iniciar sesión, inténtelo de nuevo más tarde")

    return render_template("auth/login.html")

# Ruta de logout
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

# Ruta de registro
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            existing_user = db.usuarios.find_one({"email": email})
            if existing_user:
                return render_template("auth/register.html", error="Este email ya está registrado")

            hashed_password = generate_password_hash(password)
            db.usuarios.insert_one({"username": username, "email": email, "password": hashed_password})

            return redirect(url_for("auth.login"))
        except Exception as e:
            return render_template("auth/register.html", error="No se pudo registrar el usuario, inténtelo de nuevo más tarde")

    return render_template("auth/register.html")