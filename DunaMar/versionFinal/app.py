from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from models import db, Usuario, Habitacion
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from datetime import datetime
import requests
import re
from sqlalchemy import select

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def validar_contraseña_fuerte(contraseña):
    patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(patron, contraseña) is not None

@login_manager.user_loader
def load_user(user_id):
    try:
        with db.session() as session:
            return session.get(Usuario, int(user_id))
    except Exception as e:
        app.logger.exception("Error cargando usuario")
        return None

@app.route('/')
def index():
    try:
        with db.session() as session:
            habitaciones = session.scalars(select(Habitacion)).all()
        return render_template('index.html', habitaciones=habitaciones)
    except Exception as e:
        app.logger.exception("Error cargando habitaciones")
        flash("Error al cargar las habitaciones.", "error")
        return render_template('index.html', habitaciones=[])

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre'].strip()
            email = request.form['email'].strip().lower()
            contraseña_raw = request.form['contraseña']

            with db.session() as session:
                usuario_existente = session.scalars(select(Usuario).filter_by(email=email)).first()
            if usuario_existente:
                flash("Ya existe una cuenta con ese correo electrónico.", "error")
                return redirect(url_for('registro'))

            if not validar_contraseña_fuerte(contraseña_raw):
                flash("La contraseña no cumple con los requisitos mínimos.", "error")
                return redirect(url_for('registro'))

            contraseña = generate_password_hash(contraseña_raw)
            nuevo_usuario = Usuario(nombre=nombre, email=email, contraseña=contraseña)
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            app.logger.exception("Error en el registro")
            flash("Error al registrar el usuario.", "error")
            return redirect(url_for('registro'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            contraseña = request.form['contraseña']
            with db.session() as session:
                usuario = session.scalars(select(Usuario).filter_by(email=email)).first()
            if usuario and check_password_hash(usuario.contraseña, contraseña):
                login_user(usuario)
                return redirect(url_for('index'))
            flash("Credenciales incorrectas.", "error")
        except Exception as e:
            app.logger.exception("Error en el login")
            flash("Error interno al iniciar sesión.", "error")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        app.logger.exception("Error al cerrar sesión")
        flash("Error al cerrar sesión.", "error")
    return redirect(url_for('index'))

@app.route('/configuracion')
@login_required
def configuracion():
    return render_template('configuracion.html')

@app.route('/solicitar_reserva', methods=['POST'])
@login_required
def solicitar_reserva():
    try:
        habitacion_id = int(request.form['habitacion_id'])
        fecha_entrada = datetime.strptime(request.form['fecha_entrada'], '%Y-%m-%d').date()
        fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d').date()

        with db.session() as session:
            habitacion = session.get(Habitacion, habitacion_id)

        if not habitacion:
            flash("La habitación no existe.", "error")
            return redirect(url_for('index'))

        payload = {
            "usuario": current_user.nombre,
            "email": current_user.email,
            "habitacion_id": habitacion_id,
            "habitacion_nombre": habitacion.nombre,
            "habitacion_numero": habitacion.numero,
            "fecha_entrada": fecha_entrada.isoformat(),
            "fecha_salida": fecha_salida.isoformat()
        }

        try:
            response = requests.post(Config.N8N_WEBHOOK_URL, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            app.logger.warning(f"No se pudo enviar la solicitud a n8n: {e}")
            mensaje = "No se pudo enviar la solicitud. Inténtalo más tarde."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": mensaje}), 500
            flash(mensaje, "error")
            return redirect(url_for('detalle_habitacion', habitacion_id=habitacion_id))

        mensaje = "Tu solicitud ha sido enviada. El administrador se pondrá en contacto contigo."
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"message": mensaje}), 200
        flash(mensaje, "success")

    except Exception as e:
        app.logger.exception("Error al procesar la solicitud")
        mensaje = "Hubo un error al enviar tu solicitud."
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                "message": mensaje,
                "redirect": url_for('detalle_habitacion', habitacion_id=habitacion_id)
            }), 200
        flash(mensaje, "error")

    return redirect(url_for('detalle_habitacion', habitacion_id=habitacion_id))

@app.route('/habitacion/<int:habitacion_id>')
def detalle_habitacion(habitacion_id):
    try:
        with db.session() as session:
            habitacion = session.get(Habitacion, habitacion_id)

        if not habitacion:
            flash("La habitación no existe.", "error")
            return redirect(url_for('index'))

        return render_template('detalle_habitacion.html', habitacion=habitacion)
    except Exception as e:
        app.logger.exception("Error cargando detalle de habitación")
        flash("Error al cargar la habitación.", "error")
        return redirect(url_for('index'))

@app.route('/robots.txt')
def robots_txt():
    lines = [
        "User-agent: *",
        "Disallow: /configuracion",
        "Disallow: /logout",
        "Disallow: /solicitar_reserva",
        "Sitemap: https://apartamentosdunamar.com/sitemap.xml"
    ]
    return "\n".join(lines), 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap_xml():
    try:
        with db.session() as session:
            habitaciones = session.scalars(select(Habitacion)).all()

        urls = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '  <url><loc>https://apartamentosdunamar.com/</loc></url>',
            '  <url><loc>https://apartamentosdunamar.com/registro</loc></url>',
            '  <url><loc>https://apartamentosdunamar.com/login</loc></url>',
        ]

        for h in habitaciones:
            urls.append(f'  <url><loc>https://apartamentosdunamar.com/habitacion/{h.id}</loc></url>')

        urls.append('</urlset>')
        return "\n".join(urls), 200, {'Content-Type': 'application/xml'}

    except Exception as e:
        app.logger.exception("Error generando sitemap")
        return "Error generando sitemap", 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True)