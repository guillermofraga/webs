from flask import Flask, render_template, request, redirect, url_for
from reservas import Hotel, Habitacion, Reserva, Cliente, SistemaReservas

app = Flask(__name__)

sistema = SistemaReservas()
hotel1 = Hotel("Apartamentos Duna Mar", "Sanxenxo")
sistema.registrar_hotel(hotel1)

@app.route('/')
def index():
    return render_template('index.html', hoteles=sistema.hoteles)

@app.route('/hoteles')
def hoteles():
    return render_template('hoteles.html', hoteles=sistema.hoteles)

@app.route('/agregar_hotel', methods=['POST'])
def agregar_hotel():
    nombre = request.form['nombre']
    ubicacion = request.form['ubicacion']
    if nombre and ubicacion:
        nuevo_hotel = Hotel(nombre, ubicacion)
        sistema.registrar_hotel(nuevo_hotel)
    return redirect(url_for('hoteles')) 

@app.route("/eliminar_hotel/<int:index>")
def eliminar_hotel(index):
    if 0 <= index < len(sistema.hoteles):
        hotel = sistema.hoteles[index]
        sistema.eliminar_hotel(hotel)
        return redirect(url_for('hoteles'))

@app.route('/habitaciones')
def habitaciones():
    habitaciones = []
    for hotel in sistema.hoteles:
        habitaciones.extend(hotel.habitaciones)
    return render_template('habitaciones.html', habitaciones=habitaciones, hoteles=sistema.hoteles)

@app.route('/agregar_habitacion', methods=['POST'])
def agregar_habitacion():
    hotel_nombre = request.form['hotel']
    numero = int(request.form['numero'])
    tipo = request.form['tipo']
    precio = float(request.form['precio'])
    if hotel_nombre and numero and tipo and precio:
        hotel = next((h for h in sistema.hoteles if h.nombre == hotel_nombre), None)
        if hotel:
            nueva_habitacion = Habitacion(numero, tipo, precio)
            hotel.añadir_habitacion(nueva_habitacion)
    return redirect(url_for('habitaciones'))

@app.route("/eliminar_habitacion/<int:index>")
def eliminar_habitacion(index):
    habitaciones = []
    for hotel in sistema.hoteles:
        habitaciones.extend(hotel.habitaciones)
    if 0 <= index < len(habitaciones):
        habitacion = habitaciones[index]
        for hotel in sistema.hoteles:
            if habitacion in hotel.habitaciones:
                hotel.eliminar_habitacion(habitacion)
                break
    return redirect(url_for('habitaciones'))


@app.route("/clientes")
def clientes():
    return render_template("clientes.html", clientes=sistema.clientes)

@app.route("/agregar_cliente", methods=["POST"])
def agregar_cliente():
    nombre = request.form["nombre"]
    email = request.form["email"]
    if nombre and email:
        nuevo_cliente = Cliente(len(sistema.clientes) + 1, nombre, email)
        sistema.registrar_cliente(nuevo_cliente)
    return redirect(url_for("clientes"))


@app.route("/reservas")
def reservas():
    reservas = []
    for cliente in sistema.clientes:
        reservas.extend(cliente.reservas)
    return render_template("reservas.html", 
                           reservas=reservas, 
                           habitaciones=[hab for hotel in sistema.hoteles for hab in hotel.habitaciones],
                           clientes=sistema.clientes)

@app.route("/agregar_reserva", methods=["POST"])
def agregar_reserva():
    habitacion_numero = int(request.form["habitacion"])
    cliente_nombre = request.form["cliente"]
    fecha_entrada = request.form["fecha_entrada"]
    fecha_salida = request.form["fecha_salida"]
    if habitacion_numero and cliente_nombre and fecha_entrada and fecha_salida:
        habitacion = None
        for hotel in sistema.hoteles:
            for hab in hotel.habitaciones:
                if hab.numero == int(habitacion_numero):
                    habitacion = hab
                    break
        cliente = next((c for c in sistema.clientes if c.nombre == cliente_nombre), None)
        if habitacion and cliente:
            nueva_reserva = Reserva(len(cliente.reservas) + 1, habitacion, cliente, fecha_entrada, fecha_salida)
            cliente.realizar_reserva(nueva_reserva)
    return redirect(url_for("reservas"))


@app.route("/eliminar_reserva/<int:index>")
def eliminar_reserva(index):
    reservas = []
    for cliente in sistema.clientes:
        reservas.extend(cliente.reservas)
    if 0 <= index < len(reservas):
        reserva = reservas[index]
        cliente = reserva.cliente
        cliente.cancelar_reserva(reserva)
    return redirect(url_for("reservas"))


if __name__ == '__main__':
    app.run(debug=True)