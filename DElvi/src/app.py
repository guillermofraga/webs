from flask import Flask, request, jsonify, render_template, flash, redirect, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import date, datetime, time, timedelta
from flask_mail import Mail, Message
from config import Config
from models import Reserva, db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail = Mail(app)

# Función para enviar correo de confirmación
def enviar_confirmacion(email, codigo_unico):
    msg = Message(
        subject="Confirmación de reserva",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    # Renderizamos la plantilla con Jinja2
    msg.html = render_template("email_confirmacion.html",email=email, codigo_unico=codigo_unico)
    mail.send(msg)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/reservas", methods=["POST"])
def crear_reserva():
    try:
        data = request.get_json()
        nombre = (data.get("nombre") or "").strip()
        telefono = (data.get("telefono") or "").strip()
        email = (data.get("email") or "").strip()
        fecha = data.get("fecha")
        hora = data.get("hora")
        personas = data.get("personas")

        # 🔎 Validaciones
        if not nombre or len(nombre) < 2:
            return jsonify({"error": "Nombre inválido"}), 400

        if not re.match(r"^\+?\d{7,15}$", telefono):
            return jsonify({"error": "Teléfono inválido"}), 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"error": "Correo inválido"}), 400

        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        except Exception:
            return jsonify({"error": "Formato de fecha inválido (YYYY-MM-DD)"}), 400
        
        # Validar que la fecha no sea previa a hoy 
        if fecha_obj < date.today(): 
            return jsonify({"error": "La fecha no puede ser anterior al día actual"}), 400

        try:
            hora_obj = datetime.strptime(hora, "%H:%M").time()
        except Exception:
            return jsonify({"error": "Formato de hora inválido (HH:MM)"}), 400

        try:
            personas = int(personas)
            if personas < 1 or personas > 20:
                return jsonify({"error": "Número de personas inválido, min=1, max=20"}), 400
        except Exception:
            return jsonify({"error": "Número de personas inválido"}), 400

        # 🔎 Validar disponibilidad (máximo 5 reservas por fecha/hora)
        # Limita a máximo 5 reservas en un slot exacto de hora/minuto.
        total = Reserva.query.filter_by(fecha=fecha_obj, hora=hora_obj).count()
        if total >= 5:
            return jsonify({"error": "No quedan mesas disponibles en ese horario."}), 400

        # 🔎 Insertar reserva
        nueva_reserva = Reserva(
            nombre=nombre,
            telefono=telefono,
            email=email,
            fecha=fecha_obj,
            hora=hora_obj,
            personas=personas
        )
        db.session.add(nueva_reserva)
        db.session.commit()

        # 🔎 Enviar correo de confirmación
        enviar_confirmacion(email, nueva_reserva.codigo_unico)

        return jsonify({"message": "Reserva confirmada ✅"}), 201

    except Exception as e:
        return jsonify({"error": "Error interno del servidor. Inténtalo más tarde."}), 500


@app.route("/api/disponibilidad/<fecha>", methods=["GET"])
def disponibilidad(fecha):
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
    except Exception:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    # Definir rango de horas según el día de la semana
    dia_semana = fecha_obj.weekday()  # 0=lunes, 6=domingo
    if dia_semana == 1:  # martes cerrado
        return jsonify({"horarios": []})

    if dia_semana in [4, 5, 6]:  # viernes, sábado, domingo
        inicio, fin = (12, 0), (23, 30)
    else:  # lunes, miércoles, jueves
        inicio, fin = (12, 0), (18, 0)

    current = datetime.combine(fecha_obj, time(*inicio))
    end = datetime.combine(fecha_obj, time(*fin))

    horarios = []
    while current <= end:
        hora_str = current.strftime("%H:%M")
        total = Reserva.query.filter_by(fecha=fecha_obj, hora=current.time()).count()
        disponible = total < 2  # máximo 2 reservas por slot
        horarios.append({"hora": hora_str, "disponible": disponible})
        current += timedelta(minutes=30)

    return jsonify({"horarios": horarios})


@app.route("/cancelar/<codigo>", methods=["GET", "POST"])
def cancelar(codigo):
    if request.method == "GET":
        reserva = Reserva.query.filter_by(codigo_unico=codigo).first()
        
        if not reserva:
            return render_template("cancelar.html", reserva=None)

        # Combinar fecha y hora de la reserva 
        fecha_reserva = datetime.combine(reserva.fecha, reserva.hora) 
        # Si ya pasó la fecha/hora, no permitir cancelación 
        if datetime.now() >= fecha_reserva: 
            return render_template("cancelar.html", reserva=None, error="La reserva ya ha pasado de la hora de expiración y no puede cancelarse.") 

        return render_template("cancelar.html", reserva=reserva)

    elif request.method == "POST":
        reserva = Reserva.query.filter_by(codigo_unico=codigo).first()
        if not reserva:
            return redirect(url_for("cancelar", codigo=codigo))

        # Combinar fecha y hora de la reserva 
        fecha_reserva = datetime.combine(reserva.fecha, reserva.hora) 
        # Si ya pasó la fecha/hora, no permitir cancelación 
        if datetime.now() >= fecha_reserva: 
            return render_template("cancelar.html", reserva=None, error="La reserva ya ha pasado de la hora de expiración y no puede cancelarse.") 
        
        # Si todavía no ha pasado, cancelar la reserva
        db.session.delete(reserva)
        db.session.commit()

        # Redirigimos con confirmacion=ok
        flash("Reserva cancelada exitosamente.", "success")
        return redirect(url_for("cancelar", codigo=codigo))

# Rutas para archivos estáticos especiales 
@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")


# Manejo de errores personalizados
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(403)
def handle_errors(e):
    # e.code devuelve el código (404, 500, 403)
    # e.description devuelve el mensaje por defecto
    return render_template("error.html", code=e.code, message=e.description), e.code


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])