from flask import Flask, jsonify, render_template, request, url_for
from config import Config
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

# Función para enviar correo de confirmación
def enviar_confirmacion(name, email, message):
    msg = Message(
        subject="Lead recibido - StopRend",
        sender=app.config['MAIL_USERNAME'],
        recipients=[app.config['MAIL_USERNAME']]
    )
    # Renderizamos la plantilla con Jinja2
    msg.html = render_template("email_confirmacion.html", name=name, email=email, message=message)
    mail.send(msg)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    try:
        enviar_confirmacion(name, email, message)
        return jsonify({'success': True, 'message': 'Mensaje enviado correctamente. Gracias por contactarnos!'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al enviar el mensaje, inténtalo de nuevo más tarde.'})

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)