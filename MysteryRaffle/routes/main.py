from flask import Blueprint, render_template, send_from_directory

STATICFOLDER = '../static'  # Define la ruta a la carpeta de archivos estáticos

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    return render_template("index.html")

# Rutas para archivos estáticos especiales
@main_bp.route("/robots.txt")
def robots():
    return send_from_directory(STATICFOLDER, "robots.txt")

@main_bp.route("/sitemap.xml")
def sitemap():
    return send_from_directory(STATICFOLDER, "sitemap.xml")