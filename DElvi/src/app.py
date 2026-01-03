from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import date, datetime
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


@app.route("/cancelar/<codigo>", methods=["GET", "POST"])
def cancelar(codigo):
    if request.method == "GET":
        # Si viene con confirmacion=ok, mostramos solo el mensaje de éxito
        if request.args.get("confirmacion") == "ok":
            return render_template("cancelar.html", reserva=None, confirmacion=True)

        # Caso normal: mostrar la reserva para confirmar
        reserva = Reserva.query.filter_by(codigo_unico=codigo).first()
        if not reserva:
            return render_template("cancelar.html", reserva=None)

        return render_template("cancelar.html", reserva=reserva)

    elif request.method == "POST":
        reserva = Reserva.query.filter_by(codigo_unico=codigo).first()
        if not reserva:
            return redirect(url_for("cancelar", codigo=codigo))

        db.session.delete(reserva)
        db.session.commit()

        # Redirigimos con confirmacion=ok
        return redirect(url_for("cancelar", codigo=codigo, confirmacion="ok"))
    

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])