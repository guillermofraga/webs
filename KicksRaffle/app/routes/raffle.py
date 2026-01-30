from flask import Blueprint, render_template
import stripe
from config import Config


raffle_bp = Blueprint('raffle', __name__, url_prefix='/raffle')

stripe.api_key = Config.STRIPE_SECRET_KEY

'''
@raffle_bp.route('/viewRaffle', methods=['GET'])
def view_raffle():
    return render_template("viewRaffle.html")

@raffle_bp.route('/purchaseRaffle', methods=['POST'])
def purchase_raffle():
    return render_template("purchaseRaffle.html")
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