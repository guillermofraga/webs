from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import re
from datetime import date, datetime, timedelta

app = Flask(__name__)

# Cadena de conexión en una sola línea
try:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL_DELVI", "mysql://root@localhost/delvi")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
except Exception as e:
    print(f"Error al configurar la base de datos: {e}")

db = SQLAlchemy(app)

# Modelo de la tabla reservas
class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    personas = db.Column(db.Integer, nullable=False)

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

        # Calcular rango de 1 hora
        hora_obj = datetime.strptime(hora, "%H:%M").time()
        hora_inicio = datetime.combine(fecha_obj, hora_obj)
        hora_fin = hora_inicio + timedelta(hours=1)

        # Contar reservas en esa franja
        # Limita a máximo 10 reservas en una franja de 1 hora (ej. de 12:00 a 12:59).
        reservas_en_hora = Reserva.query.filter(
            Reserva.fecha == fecha_obj,
            Reserva.hora >= hora_inicio.time(),
            Reserva.hora < hora_fin.time()
        ).count()

        if reservas_en_hora >= 10:
            return jsonify({"error": "Todas las mesas en esa franja horaria ya están reservadas"}), 400

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

        # 🔎 Validar disponibilidad (máximo 10 reservas por fecha/hora)
        # Limita a máximo 10 reservas en un slot exacto de hora/minuto.
        total = Reserva.query.filter_by(fecha=fecha_obj, hora=hora_obj).count()
        if total >= 10:
            return jsonify({"message": "No quedan mesas disponibles en ese horario."}), 400

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

        return jsonify({"message": "Reserva confirmada ✅"}), 201

    except Exception as e:
        return jsonify({"error": "Error interno del servidor. Inténtalo más tarde."}), 500

if __name__ == "__main__":
    app.run(debug=True)