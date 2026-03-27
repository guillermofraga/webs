from flask import Flask, render_template
from config import Config
from models import Reserva, db
from datetime import datetime, date, time, timedelta
import re
import uuid
from flask import request, jsonify, redirect, url_for, flash
from flask import send_from_directory
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail = Mail(app)

# Función para enviar correo de confirmación
def enviar_confirmacion(email, reserva):
    cancel_url = url_for("cancelar", codigo=reserva.codigo_unico, _external=True)
    msg = Message(
        subject="Confirmación de reserva",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email],
    )
    # Renderizamos la plantilla con Jinja2
    msg.html = render_template(
        "email_confirmacion.html",
        email=email,
        reserva=reserva,
        cancel_url=cancel_url,
    )
    mail.send(msg)


def enviar_solicitud_propietario(reserva):
    """
    Envía un correo al propietario con 2 botones para aceptar o cancelar.
    """
    owner_email = app.config.get("OWNER_EMAIL")
    if not owner_email:
        raise ValueError("OWNER_EMAIL no está configurado")

    accept_url = url_for("propietario_aceptar", codigo=reserva.codigo_unico, _external=True)
    cancel_url = url_for("propietario_cancelar", codigo=reserva.codigo_unico, _external=True)

    msg = Message(
        subject="Reserva pendiente de confirmación",
        sender=app.config["MAIL_USERNAME"],
        recipients=[owner_email],
    )
    msg.html = render_template(
        "propietario_confirmar.html",
        reserva=reserva,
        accept_url=accept_url,
        cancel_url=cancel_url,
    )
    mail.send(msg)


def enviar_cancelacion_usuario(email, reserva):
    """
    Envía un correo al usuario cuando el propietario cancela la reserva.
    """
    msg = Message(
        subject="Reserva cancelada",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email],
    )
    msg.html = render_template("email_reserva_cancelada.html", reserva=reserva)
    mail.send(msg)


def enviar_cancelacion_propietario(reserva):
    """
    Envía un correo al propietario cuando el cliente cancela una reserva.
    """
    owner_email = app.config.get("OWNER_EMAIL")
    if not owner_email:
        raise ValueError("OWNER_EMAIL no está configurado")

    msg = Message(
        subject="Reserva cancelada por el cliente",
        sender=app.config["MAIL_USERNAME"],
        recipients=[owner_email],
    )
    msg.html = render_template("propietario_reserva_cancelada.html", reserva=reserva)
    mail.send(msg)


def get_last_week_range():
    """
    Devuelve (week_start, week_end) de la semana anterior en formato calendario,
    usando lunes->domingo.
    """
    today = date.today()
    week_start_this = today - timedelta(days=today.weekday())  # lunes de esta semana
    week_start_last = week_start_this - timedelta(days=7)  # lunes semana anterior
    week_end_last = week_start_last + timedelta(days=6)  # domingo semana anterior
    return week_start_last, week_end_last


def enviar_reporte_semanal_propietario():
    """
    Envía un correo semanal al propietario (OWNER_EMAIL) y también a MAIL_USERNAME,
    con las reservas de la semana anterior (lunes-domingo).

    Nota: como la BD no guarda 'asistió/no asistió', se contabilizan las reservas
    que siguen en el sistema (no canceladas).
    """
    owner_email = app.config.get("OWNER_EMAIL")
    mail_username = app.config.get("MAIL_USERNAME")
    if not owner_email or not mail_username:
        raise ValueError("Faltan OWNER_EMAIL o MAIL_USERNAME para enviar el reporte.")

    week_start, week_end = get_last_week_range()

    reservas = (
        Reserva.query.filter(Reserva.fecha >= week_start, Reserva.fecha <= week_end)
        .order_by(Reserva.fecha.asc(), Reserva.hora.asc())
        .all()
    )

    mesas = len(reservas)
    total_eur = mesas * 2

    recipients = []
    if owner_email:
        recipients.append(owner_email)
    if mail_username and mail_username not in recipients:
        recipients.append(mail_username)

    msg = Message(
        subject=f"Reporte semanal Mocca ({week_start.strftime('%d/%m')} - {week_end.strftime('%d/%m')})",
        sender=mail_username,
        recipients=recipients,
    )

    msg.html = render_template(
        "reporte_semanal_propietario.html",
        reservas=reservas,
        mesas=mesas,
        total_eur=total_eur,
        week_start=week_start,
        week_end=week_end,
    )
    mail.send(msg)


@app.route("/api/reportes/semanal", methods=["POST"])
def api_reporte_semanal():
    """
    Endpoint para ejecutar el reporte semanal desde un cron/Task Scheduler.
    """
    cron_secret = app.config.get("CRON_SECRET")
    provided = request.headers.get("X-CRON-SECRET") or request.args.get("secret")

    if cron_secret and provided != cron_secret:
        return jsonify({"error": "No autorizado"}), 403
    if not cron_secret:
        # Proteccion básica: si no hay token configurado, rechazamos.
        return jsonify({"error": "CRON_SECRET no configurado"}), 403

    try:
        enviar_reporte_semanal_propietario()
    except Exception:
        return jsonify({"error": "No se pudo enviar el reporte semanal."}), 500

    return jsonify({"message": "Reporte enviado ✅"}), 200

@app.route("/")
def index():
    return render_template("index.html")

# API para crear una reserva
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

        # 🔎 Insertar reserva (pendiente hasta decisión del propietario)
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

        # 🔎 Enviar solicitud al propietario para que decida
        try:
            enviar_solicitud_propietario(nueva_reserva)
            return jsonify(
                {"message": "Solicitud enviada ✅. El propietario la confirmará en breve."}
            ), 201
        except Exception:
            # Si falla el envío (config o mail), no rompemos la reserva.
            return jsonify(
                {"message": "Reserva creada, pero no se pudo notificar al propietario (configuración incompleta)."}
            ), 201

    except Exception as e:
        return jsonify({"error": "Error interno del servidor. Inténtalo más tarde."}), 500

# API para obtener la disponibilidad de las mesas
@app.route("/api/disponibilidad/<fecha>", methods=["GET"])
def disponibilidad(fecha):
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        if fecha_obj < date.today():
            return jsonify({"error": "La fecha no puede ser anterior al día actual"}), 400
    except Exception:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    # Definir rango de horas según el día de la semana
    dia_semana = fecha_obj.weekday()  # 0=lunes, 6=domingo
    if dia_semana == 1:  # martes cerrado
        return jsonify({"horarios": []})

    if dia_semana in [0, 1, 2, 3, 4, 5]:  # lunes, martes, miércoles, jueves, viernes, sábado
        inicio, fin = (12, 30), (22, 30)
    else:  # domingo
        inicio, fin = (12, 30), (15, 30)

    current = datetime.combine(fecha_obj, time(*inicio))
    end = datetime.combine(fecha_obj, time(*fin))

    horarios = []
    ahora = datetime.now()
    while current <= end:
        # Si el usuario consulta "hoy", no mostramos horas ya pasadas
        # (ej: si son > 14:00, no aparecerán 12:30, 13:00, 13:30, 14:00)
        if fecha_obj == ahora.date() and current.time() < ahora.time():
            current += timedelta(minutes=30)
            continue

        hora_str = current.strftime("%H:%M")
        total = Reserva.query.filter_by(fecha=fecha_obj, hora=current.time()).count()
        disponible = total < 4  # máximo 4 reservas por slot
        horarios.append({"hora": hora_str, "disponible": disponible})
        current += timedelta(minutes=30)

    return jsonify({"horarios": horarios})


# Endpoint para re-enviar la solicitud al propietario (útil para pruebas/reenviar)
@app.route("/api/propietario/solicitar-confirmacion/<codigo>", methods=["POST"])
def solicitar_confirmacion_propietario(codigo):
    reserva = Reserva.query.filter_by(codigo_unico=codigo).first()
    if not reserva:
        return jsonify({"error": "Reserva no encontrada"}), 404

    try:
        enviar_solicitud_propietario(reserva)
    except ValueError as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Solicitud enviada al propietario ✅"}), 200


@app.route("/propietario/aceptar/<codigo>", methods=["GET"])
def propietario_aceptar(codigo):
    reserva = Reserva.query.filter_by(codigo_unico=codigo).first()
    if not reserva:
        return render_template("error.html", code=404, message="Reserva no encontrada."), 404

    try:
        # Invalidar inmediatamente los enlaces del propietario para que
        # aceptar/cancelar solo se pueda ejecutar una vez.
        reserva.codigo_unico = str(uuid.uuid4())

        enviar_confirmacion(reserva.email, reserva)

        db.session.commit()
    except Exception:
        db.session.rollback()
        # Si falla el email, no cancelamos la reserva; devolvemos error.
        return render_template("error.html", code=500, message="No se pudo enviar el correo de confirmación."), 500

    return render_template(
        "propietario_resultado.html",
        title="Reserva aceptada",
        message="La confirmación se ha enviado al cliente por correo.",
        icon="check_circle",
        icon_color="text-green-600",
        title_color="text-green-700 dark:text-green-400",
        reserva=reserva,
    ), 200


@app.route("/propietario/cancelar/<codigo>", methods=["GET"])
def propietario_cancelar(codigo):
    reserva = Reserva.query.filter_by(codigo_unico=codigo).first()
    if not reserva:
        return render_template("error.html", code=404, message="Reserva no encontrada."), 404

    # Combinar fecha y hora de la reserva
    fecha_reserva = datetime.combine(reserva.fecha, reserva.hora)

    # Si ya pasó la fecha/hora, no permitir cancelación
    if datetime.now() >= fecha_reserva:
        return render_template(
            "error.html",
            code=400,
            message="La reserva ya ha pasado de la hora de expiración y no puede cancelarse.",
        ), 400

    try:
        enviar_cancelacion_usuario(reserva.email, reserva)
    except Exception:
        # Si falla el email, tampoco borramos la reserva para evitar pérdidas silenciosas.
        return render_template("error.html", code=500, message="No se pudo enviar el correo de cancelación."), 500

    try:
        db.session.delete(reserva)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return render_template("error.html", code=500, message="No se pudo cancelar la reserva en el sistema."), 500

    return render_template(
        "propietario_resultado.html",
        title="Reserva cancelada",
        message="Se ha notificado al cliente por correo y la reserva se ha eliminado del sistema.",
        icon="cancel",
        icon_color="text-red-600",
        title_color="text-red-700 dark:text-red-400",
        reserva=reserva,
    ), 200

# Rutas para cancelar una reserva
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
        try:
            db.session.delete(reserva)
            db.session.commit()

            # Notificar al propietario de la cancelación
            try:
                enviar_cancelacion_propietario(reserva)
            except Exception:
                # No bloqueamos la cancelación si falla el email
                pass

            flash("Reserva cancelada exitosamente.", "success")
        except Exception as e:
            db.session.rollback()

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

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)