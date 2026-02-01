from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@main_bp.route("/fecha-final", methods=['GET'])
def fecha_final():
    # Aquí se define la fecha final de la votación
    fecha_final = "2026-02-31T23:59:59Z"
    return {"fechaFinal": fecha_final}