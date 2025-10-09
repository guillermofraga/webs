
# Clase Hotel
class Hotel:
    def __init__(self, nombre, ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.habitaciones = []

    def añadir_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)
        print(f"Habitacion {habitacion.numero} añadida al hotel {self.nombre}")

    def eliminar_habitacion(self, habitacion):
        self.habitaciones.remove(habitacion)
        print(f"Habitacion {habitacion.numero} eliminada del hotel {self.nombre}")

    def buscar_habitacion(self, tipo=None, precio_max=None):
        resultados = []
        for habitacion in self.habitaciones:
            if (tipo is None or habitacion.tipo == tipo) and (precio_max is None or habitacion.precio <= precio_max):
                resultados.append(habitacion)
        return resultados
    def mostrar_info(self):
        return f"Hotel: {self.nombre}, Ubicado en {self.ubicacion}"

# Clase Habitacion
class Habitacion:
    def __init__(self, numero, tipo, precio):
        self.numero = numero
        self.tipo = tipo
        self.precio = precio
        self.disponible = True

    def actualizar_disponibilidad(self, disponible):
        self.disponible = disponible
        estado = "disponible" if disponible else "no disponible" # si disponible es True, estado es "disponible", si es False, estado es "no disponible"
        print(f"Habitación {self.numero} ahora está {estado}")

    def mostrar_info(self):
        return f"Habitación {self.numero}, Tipo: {self.tipo}, Precio: {self.precio} por noche"

# Clase Reserva
class Reserva:
    def __init__(self, id_reserva, habitacion, cliente, fecha_entrada, fecha_salida):
        self.id_reserva = id_reserva
        self.habitacion = habitacion
        self.cliente = cliente
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.estado = "pendiente"

    def modificar_reserva(self, nueva_fecha_entrada, nueva_fecha_salida):
        self.fecha_entrada = nueva_fecha_entrada
        self.fecha_salida = nueva_fecha_salida
        print(f"""Reserva {self.id_reserva} modificada para el período {self.fecha_entrada} a {self.fecha_salida}.""")

    def cancelar_reserva(self):
        self.estado = "cancelada"
        self.habitacion.actualizar_disponibilidad(True)
        print(f"Reserva {self.id_reserva} cancelada.")

# Clase Cliente
class Cliente:
    def __init__(self, id_cliente, nombre, email):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.reservas = []

    def realizar_reserva(self, reserva):
        self.reservas.append(reserva)
        reserva.estado = "confirmada"
        reserva.habitacion.actualizar_disponibilidad(False)
        print(f"""Reserva {reserva.id_reserva} realizada por {self.nombre} para la habitación {reserva.habitacion.numero}.""")

    def cancelar_reserva(self, reserva):
        if reserva in self.reservas:
            reserva.cancelar_reserva()
            self.reservas.remove(reserva)

# Clase SistemaReservas
class SistemaReservas:
    def __init__(self):
        self.hoteles = []
        self.clientes = []

    def registrar_hotel(self, hotel):
        self.hoteles.append(hotel)
        print(f"Hotel: {hotel.nombre} registrado en el sistema.")

    def eliminar_hotel(self, hotel):
        self.hoteles.remove(hotel)
        print(f"Hotel {hotel.nombre} eliminado del sistema.")

    def registrar_cliente(self, cliente):
        self.clientes.append(cliente)
        print(f"Cliente {cliente.nombre} registrado en el sistema.")

    def eliminar_cliente(self, cliente):
        self.clientes.remove(cliente)
        print(f"Cliente {cliente.nombre} eliminado del sistema.")

    def buscar_hoteles(self, ubicacion=None, nombre=None):
        resultados = []
        for hotel in self.hoteles:
            if (ubicacion is None or hotel.ubicacion == ubicacion) and (nombre is None or hotel.nombre == nombre):
                resultados.append(hotel)
        return resultados

    def listar_reservas(self):
        for cliente in self.clientes:
            for reserva in cliente.reservas:
                print(f"Reserva: {reserva.id_reserva} para el cliente: {cliente.nombre}, Habitación Reservada: {reserva.habitacion.numero}, para las fechas desde: {reserva.fecha_entrada}, hasta: {reserva.fecha_salida} y Estado: {reserva.estado}.")


# Main

# Crear una instanca de SistemaReservas
sistema = SistemaReservas()

# Crear un hotel
hotel1 = Hotel("Hotel Duna Mar", "Sanxenxo")

print(sistema.buscar_hoteles("Sanxenxo"))

# Registrar el hotel en el sistema
sistema.registrar_hotel(hotel1)

print(sistema.buscar_hoteles("Sanxenxo"))

print(sistema.hoteles[0].nombre)

hotel1.habitaciones

# Añadir habitaciones al hotel
habitacion1 = Habitacion(101, "Estudio", 70)
habitacion2 = Habitacion(102, "Una Habitación", 120)
habitacion3 = Habitacion(102, "Dos Habitaciones", 170)
habitacion4 = Habitacion(103, "Ático", 220)

hotel1.añadir_habitacion(habitacion1)
hotel1.añadir_habitacion(habitacion2)
hotel1.añadir_habitacion(habitacion3)
hotel1.añadir_habitacion(habitacion4)

hotel1.habitaciones

#Crear cliente
Cliente1 = Cliente(1, "Alice Johnson", "alice@example.com")
Cliente2 = Cliente(2, "Bob Smith", "bob@example.com")

#Registrar clientes en el sistema
sistema.registrar_cliente(Cliente1)
sistema.registrar_cliente(Cliente2)

# Cliente1 Hace una reserva
reserva1 = Reserva(1, habitacion1, Cliente1, "2024-06-01", "2024-07-05")
print(reserva1.estado)
Cliente1.realizar_reserva(reserva1)

# Cliente 2 Hace una reserva
reserva2 = Reserva(2, habitacion3, Cliente2, "2024-06-10", "2024-06-15")
Cliente2.realizar_reserva(reserva2)

sistema.listar_reservas()

# Modificar una reserva
reserva1.modificar_reserva("2024-06-02", "2024-06-06")

sistema.listar_reservas()

# Cancelar una reserva
reserva2.cancelar_reserva()

sistema.listar_reservas()

# Mostrar información del hotel y las habitaciones disponibles
print("\nInformación de hoteles y habitaciones:")
for hotel in sistema.hoteles:
    print(hotel.mostrar_info())
    for habitacion in hotel.habitaciones:
        disponibilidad = "Disponible" if habitacion.disponible else "No Disponible"
        print(f"  - {habitacion.mostrar_info()} - {disponibilidad}")