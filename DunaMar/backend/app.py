from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from models import db, Usuario, Habitacion, Reserva  # Hotel eliminado
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from sqlalchemy import and_, or_
from datetime import datetime

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def index():
    habitaciones = Habitacion.query.all()
    return render_template('index.html', habitaciones=habitaciones)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = generate_password_hash(request.form['contraseña'])
        if Usuario.query.filter_by(email=email).first():
            return "El usuario ya existe"
        nuevo_usuario = Usuario(nombre=nombre, email=email, contraseña=contraseña)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.contraseña, contraseña):
            login_user(usuario)
            return redirect(url_for('index'))
        return "Credenciales incorrectas"
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/configuracion')
@login_required
def configuracion():
    return render_template('configuracion.html')

@app.route('/reservas')
@login_required
def reservas():
    reservas = Reserva.query.filter_by(usuario_id=current_user.id, estado='confirmada').all()
    habitaciones = Habitacion.query.all()
    return render_template('formulario_reserva.html', reservas=reservas, habitaciones=habitaciones)

@app.route('/agregar_reserva', methods=['POST'])
@login_required
def agregar_reserva():
    habitacion_id = int(request.form['habitacion_id'])
    fecha_entrada = datetime.strptime(request.form['fecha_entrada'], '%Y-%m-%d').date()
    fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d').date()

    # Verificar si hay reservas que se solapan
    reservas_existentes = Reserva.query.filter(
        Reserva.habitacion_id == habitacion_id,
        Reserva.estado == 'confirmada',
        or_(
            and_(Reserva.fecha_entrada <= fecha_entrada, Reserva.fecha_salida > fecha_entrada),
            and_(Reserva.fecha_entrada < fecha_salida, Reserva.fecha_salida >= fecha_salida),
            and_(Reserva.fecha_entrada >= fecha_entrada, Reserva.fecha_salida <= fecha_salida)
        )
    ).all()

    if reservas_existentes:
        flash("La habitación ya está reservada en esas fechas.", "error")
        return redirect(url_for('reservas'))

    # Si está libre, crear la reserva
    nueva_reserva = Reserva(
        fecha_entrada=fecha_entrada,
        fecha_salida=fecha_salida,
        estado='confirmada',
        habitacion_id=habitacion_id,
        usuario_id=current_user.id
    )
    db.session.add(nueva_reserva)
    db.session.commit()
    flash("Reserva confirmada con éxito.", "success")
    return redirect(url_for('reservas'))

@app.route('/habitaciones_disponibles', methods=['POST'])
def habitaciones_disponibles():
    fecha_entrada = datetime.strptime(request.form['fecha_entrada'], '%Y-%m-%d').date()
    fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d').date()

    # Buscar habitaciones que NO tengan reservas confirmadas en ese rango
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

@app.route('/habitacion/<int:habitacion_id>')
def detalle_habitacion(habitacion_id):
    habitacion = Habitacion.query.get_or_404(habitacion_id)
    return render_template('detalle_habitacion.html', habitacion=habitacion)

@app.route('/mis_reservas')
@login_required
def mis_reservas():
    reservas = Reserva.query.filter_by(usuario_id=current_user.id).order_by(Reserva.fecha_entrada.desc()).all()
    return render_template('mis_reservas.html', reservas=reservas)

@app.route('/cancelar_reserva/<int:reserva_id>')
@login_required
def cancelar_reserva(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)

    if reserva.usuario_id != current_user.id:
        flash("No tienes permiso para cancelar esta reserva.", "error")
        return redirect(url_for('mis_reservas'))

    reserva.estado = 'cancelada'
    db.session.commit()
    flash("Reserva cancelada correctamente.", "success")
    return redirect(url_for('mis_reservas'))

@app.route('/formulario_reserva/<int:habitacion_id>', methods=['GET', 'POST'])
@login_required
def formulario_reserva(habitacion_id):
    habitacion = Habitacion.query.get_or_404(habitacion_id)

    if request.method == 'POST':
        fecha_entrada = datetime.strptime(request.form['fecha_entrada'], '%Y-%m-%d').date()
        fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d').date()

        # Verificar disponibilidad
        reservas_existentes = Reserva.query.filter(
            Reserva.habitacion_id == habitacion_id,
            Reserva.estado == 'confirmada',
            or_(
                and_(Reserva.fecha_entrada <= fecha_entrada, Reserva.fecha_salida > fecha_entrada),
                and_(Reserva.fecha_entrada < fecha_salida, Reserva.fecha_salida >= fecha_salida),
                and_(Reserva.fecha_entrada >= fecha_entrada, Reserva.fecha_salida <= fecha_salida)
            )
        ).all()

        if reservas_existentes:
            flash("La habitación ya está reservada en esas fechas.", "error")
            return redirect(url_for('detalle_habitacion', habitacion_id=habitacion_id))

        nueva_reserva = Reserva(
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            estado='confirmada',
            habitacion_id=habitacion_id,
            usuario_id=current_user.id
        )
        db.session.add(nueva_reserva)
        db.session.commit()
        flash("Reserva confirmada con éxito.", "success")
        return redirect(url_for('mis_reservas'))

    return render_template('detalle_habitacion.html', habitacion=habitacion)

@app.route('/fechas_ocupadas/<int:habitacion_id>')
def fechas_ocupadas(habitacion_id):
    reservas = Reserva.query.filter_by(habitacion_id=habitacion_id, estado='confirmada').all()
    fechas = []

    for r in reservas:
        rango = (r.fecha_entrada, r.fecha_salida)
        fechas.append({
            'inicio': rango[0].isoformat(),
            'fin': rango[1].isoformat()
        })

    return jsonify(fechas)

if __name__ == '__main__':
    app.run(debug=True)