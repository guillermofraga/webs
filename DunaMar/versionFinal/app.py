from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from models import db, Usuario, Habitacion, Reserva
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
import requests
import re

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Funcion para validar la contraseña fuerte:

def validar_contraseña_fuerte(contraseña):
    """
    Verifica si la contraseña cumple con los requisitos mínimos:
    - Al menos 8 caracteres
    - Una letra mayúscula
    - Una letra minúscula
    - Un número
    - Un símbolo especial (@$!%*?&)
    """
    patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(patron, contraseña) is not None

@login_manager.user_loader
def load_user(user_id):
    try:
        return Usuario.query.get(int(user_id))
    except Exception as e:
        app.logger.exception("Error cargando usuario")
        return None

@app.route('/')
def index():
    try:
        habitaciones = Habitacion.query.all()
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

            # Verificar si el correo ya existe
            usuario_existente = Usuario.query.filter_by(email=email).first()
            if usuario_existente:
                flash("Ya existe una cuenta con ese correo electrónico.", "error")
                return redirect(url_for('registro'))

            # Validar contraseña fuerte (opcional)
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
            usuario = Usuario.query.filter_by(email=email).first()
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

@app.route('/agregar_reserva', methods=['POST'])
@login_required
def agregar_reserva():
    try:
        habitacion_id = int(request.form['habitacion_id'])
        fecha_entrada = datetime.strptime(request.form['fecha_entrada'], '%Y-%m-%d').date()
        fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d').date()

        # Preparar payload para n8n
        payload = {
            "usuario": current_user.nombre,
            "email": current_user.email,
            "habitacion_id": habitacion_id,
            "habitacion_nombre": Habitacion.query.get(habitacion_id).nombre,
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
            return redirect(url_for('reservas'))

        # No se guarda en la base de datos
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

    return redirect(url_for('detalle_habitacion',habitacion_id=habitacion_id))


@app.route('/habitaciones_disponibles', methods=['POST'])
def habitaciones_disponibles():
    try:
        fecha_entrada = datetime.strptime(request.form['fecha_entrada'], '%Y-%m-%d').date()
        fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d').date()

        subquery = Reserva.query.filter(
            Reserva.estado == 'confirmada',
            or_(
                and_(Reserva.fecha_entrada <= fecha_entrada, Reserva.fecha_salida > fecha_entrada),
                and_(Reserva.fecha_entrada < fecha_salida, Reserva.fecha_salida >= fecha_salida),
                and_(Reserva.fecha_entrada >= fecha_entrada, Reserva.fecha_salida <= fecha_salida)
            )
        ).with_entities(Reserva.habitacion_id)

        disponibles = Habitacion.query.filter(~Habitacion.id.in_(subquery)).all()

        return jsonify([
            {'id': h.id, 'numero': h.numero, 'nombre': h.nombre, 'tipo': h.tipo, 'precio': h.precio}
            for h in disponibles
        ])
    except Exception as e:
        app.logger.exception("Error buscando habitaciones disponibles")
        return jsonify({'error': 'Error interno al buscar habitaciones'}), 500

@app.route('/habitacion/<int:habitacion_id>')
def detalle_habitacion(habitacion_id):
    try:
        habitacion = Habitacion.query.get_or_404(habitacion_id)
        return render_template('detalle_habitacion.html', habitacion=habitacion)
    except Exception as e:
        app.logger.exception("Error cargando detalle de habitación")
        flash("Error al cargar la habitación.", "error")
        return redirect(url_for('index'))

@app.route('/reservas')
@login_required
def reservas():
    try:
        reservas = Reserva.query.filter(
            Reserva.usuario_id == current_user.id,
            Reserva.estado != 'cancelada'
        ).order_by(Reserva.fecha_entrada.desc()).all()
        return render_template('reservas.html', reservas=reservas)
    except Exception as e:
        app.logger.exception("Error cargando mis reservas")
        flash("Error al cargar tus reservas.", "error")
        return render_template('reservas.html', reservas=[])

@app.route('/cancelar_reserva/<int:reserva_id>')
@login_required
def cancelar_reserva(reserva_id):
    try:
        reserva = Reserva.query.get_or_404(reserva_id)

        if reserva.usuario_id != current_user.id:
            flash("No tienes permiso para cancelar esta reserva.", "error")
            return redirect(url_for('reservas'))

        # Actualizar estado
        reserva.estado = 'cancelada'
        db.session.commit()

        # Notificar a n8n
        payload = {
            "accion": "cancelar",
            "usuario": current_user.nombre,
            "email": current_user.email,
            "habitacion_nombre": reserva.habitacion.nombre,
            "habitacion_id": reserva.habitacion_id,
            "fecha_entrada": reserva.fecha_entrada.isoformat(),
            "fecha_salida": reserva.fecha_salida.isoformat(),
            "reserva_id": reserva.id
        }

        try:
            response = requests.post(Config.N8N_WEBHOOK_URL, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "success":
                app.logger.warning(f"n8n no confirmó el envío del correo de cancelación: {data}")
        except Exception as e:
            app.logger.warning(f"No se pudo notificar a n8n sobre la cancelación: {e}")

        flash("Reserva cancelada correctamente.", "success")

    except Exception as e:
        db.session.rollback()
        app.logger.exception("Error cancelando reserva")
        flash("Error al cancelar la reserva.", "error")

    return redirect(url_for('reservas'))

@app.route('/fechas_ocupadas/<int:habitacion_id>')
def fechas_ocupadas(habitacion_id):
    try:
        reservas = Reserva.query.filter_by(habitacion_id=habitacion_id, estado='confirmada').all()
        fechas_ocupadas = set()
        fechas_entrada = set()

        for reserva in reservas:
            fechas_entrada.add(reserva.fecha_entrada.isoformat())
            fecha = reserva.fecha_entrada
            while fecha < reserva.fecha_salida:
                fechas_ocupadas.add(fecha.isoformat())
                fecha += timedelta(days=1)

        return jsonify({"ocupadas": sorted(fechas_ocupadas), "entradas": sorted(fechas_entrada)})
    except Exception as e:
        app.logger.exception("Error obteniendo fechas ocupadas")
        return jsonify({'error': 'Error interno al obtener fechas'}), 500

# Manejador de errores

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