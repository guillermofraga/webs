from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import re
from datetime import datetime

app = Flask(__name__)

# Cadena de conexión en una sola línea
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL_DELVI", "mysql://root@localhost/delvi")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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

        try:
            hora_obj = datetime.strptime(hora, "%H:%M").time()
        except Exception:
            return jsonify({"error": "Formato de hora inválido (HH:MM)"}), 400

        try:
            personas = int(personas)
            if personas < 1 or personas > 20:
                return jsonify({"error": "Número de personas inválido"}), 400
        except Exception:
            return jsonify({"error": "Número de personas inválido"}), 400

        # 🔎 Validar disponibilidad (máximo 10 reservas por fecha/hora)
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
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    app.run(debug=True)