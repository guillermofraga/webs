from flask import Blueprint, render_template, request
import stripe
from config import Config
from models import Votacion, db


raffle_bp = Blueprint('raffle', __name__, url_prefix='/raffle')

stripe.api_key = Config.STRIPE_SECRET_KEY

@raffle_bp.route("/vote", methods=['POST'])
def vote():
    try:
        email = request.form.get("email")
        precio_rifa = float(request.form.get("precio_rifa"))

        if not email or not precio_rifa:
            return {'success': False, 'message': 'Por favor, completa todos los campos requeridos.'}, 400
        elif Votacion.query.filter_by(email=email).first():
            return {'success': False, 'message': 'Ya has accedido a la rifa con este correo electrónico.'}, 400
        elif precio_rifa not in [2.0, 3.0, 5.0]:
            return {'success': False, 'message': 'Precio no válido.'}, 400

        new_vote = Votacion(email=email, precio_rifa=precio_rifa)
        try:
            db.session.add(new_vote)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': 'Error al guardar el acceso. Por favor, inténtalo de nuevo más tarde.'}, 500

        return {'success': True, 'message': 'Tu acceso a la rifa ha sido registrado. Próximamente recibirás noticias.'}, 200
    except Exception as e:
        return {'success': False, 'message': 'Error al procesar el acceso.'}, 500

'''
@raffle_bp.route("/purchaseRaffle", methods=['GET', 'POST'])
def purchaseRaffle():
    try:
        # Crea PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount = 100, # convertir a céntimos
            currency="eur",
            metadata={"raffle": "zapatillas edición limitada 2026"},
        )

        return render_template(
            "purchaseRaffle.html",
            precio = f"{intent.amount / 100:.2f}", 
            client_secret=intent.client_secret,
            stripe_public_key = Config.STRIPE_PUBLIC_KEY
            )
    except Exception as e:
        return render_template("index.html", error="No se pudo realizar la reserva, intentelo de nuevo más tarde.")

@raffle_bp.route("/success")
def success():
    return render_template("pagos/success.html")

@raffle_bp.route("/cancel")
def  cancel():
    return render_template("pagos/cancel.html")
'''