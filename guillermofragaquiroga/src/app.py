from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send-email", methods=['POST'])
def send_email():
    try:
        data = request.get_json()

        # Validar que todos los campos requeridos estén presentes
        required_fields = ['asunto', 'correo', 'necesidades']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'El campo {field} es requerido'}), 400

        asunto = data.get('asunto')
        correo = data.get('correo')
        necesidades = data.get('necesidades')

        # Crear el mensaje de correo, si no se especifica un correo para enviar, se usará el correo del mail_default_sender
        msg = Message(
            subject=f'Nueva solicitud para Guillermo: {asunto}',
            recipients=[app.config['MAIL_RECIPIENTS']], # tiene que ser una lista, aunque sea un solo correo
            html=f"""
            <h2>Nueva solicitud de contacto</h2>
            <p><strong>Asunto:</strong> {asunto}</p>
            <p><strong>Correo del cliente:</strong> {correo}</p>
            <p><strong>Necesidades:</strong></p>
            <p>{necesidades.replace(chr(10), '<br>')}</p>
            """
        )

        mail.send(msg)

        return jsonify({'success': True, 'message': 'Correo enviado exitosamente'}), 200

    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
        return jsonify({'success': False, 'message': 'Error al enviar el correo'}), 500


# Rutas para archivos estáticos especiales
@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")


if __name__ == '__main__':
    app.run(debug=Config.DEBUG)