import json
import os
from datetime import date, datetime


class Hotel:
    def __init__(self, nombre):
        self.nombre = nombre
        self.habitaciones = []
        self.clientes = []
        self.reservas = []
        self.archivo_datos = os.path.join(os.path.dirname(__file__), "hotel_data.json")

        self.cargar_datos()

    def _crear_habitaciones_iniciales(self):
        self.agregar_habitacion(HabitacionEstandar(101, 120.0, 2, True))
        self.agregar_habitacion(Suite(201, 220.0, 3, True, 80.0))
        self.agregar_habitacion(HabitacionFamiliar(301, 180.0, 4, True, 50.0))

    def guardar_datos(self):
        datos = {
            "clientes": [
                {
                    "nombre": cliente.nombre,
                    "documento": cliente.documento,
                    "telefono": cliente.telefono,
                }
                for cliente in self.clientes
            ],
            "habitaciones": [
                self._serializar_habitacion(habitacion) for habitacion in self.habitaciones
            ],
            "reservas": [
                {
                    "cliente_documento": reserva.cliente.documento,
                    "habitacion_numero": reserva.habitacion.numero,
                    "fecha_entrada": reserva.fecha_entrada.isoformat(),
                    "fecha_salida": reserva.fecha_salida.isoformat(),
                    "estado": reserva.estado,
                }
                for reserva in self.reservas
            ],
        }

        with open(self.archivo_datos, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)

    def _serializar_habitacion(self, habitacion):
        datos = {
            "numero": habitacion.numero,
            "tipo": habitacion.__class__.__name__,
            "precio_por_noche": habitacion.precio_por_noche,
            "capacidad": habitacion.capacidad,
            "disponible": habitacion.disponible,
        }

        if isinstance(habitacion, Suite):
            datos["costo_extra"] = habitacion.costo_extra
        elif isinstance(habitacion, HabitacionFamiliar):
            datos["aumento_familiar"] = habitacion.aumento_familiar

        return datos

    def cargar_datos(self):
        if not os.path.exists(self.archivo_datos):
            self._crear_habitaciones_iniciales()
            return

        try:
            with open(self.archivo_datos, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            self._crear_habitaciones_iniciales()
            return

        self.clientes = []
        self.habitaciones = []
        self.reservas = []

        for cliente_datos in datos.get("clientes", []):
            self.agregar_cliente(
                Cliente(
                    cliente_datos.get("nombre", ""),
                    cliente_datos.get("documento", ""),
                    cliente_datos.get("telefono", ""),
                )
            )

        for habitacion_datos in datos.get("habitaciones", []):
            tipo = habitacion_datos.get("tipo", "HabitacionEstandar")
            numero = habitacion_datos.get("numero")
            precio = habitacion_datos.get("precio_por_noche", 0)
            capacidad = habitacion_datos.get("capacidad", 1)
            disponible = habitacion_datos.get("disponible", True)

            if tipo == "Suite":
                self.agregar_habitacion(
                    Suite(numero, precio, capacidad, disponible, habitacion_datos.get("costo_extra", 0))
                )
            elif tipo == "HabitacionFamiliar":
                self.agregar_habitacion(
                    HabitacionFamiliar(
                        numero,
                        precio,
                        capacidad,
                        disponible,
                        habitacion_datos.get("aumento_familiar", 0),
                    )
                )
            else:
                self.agregar_habitacion(HabitacionEstandar(numero, precio, capacidad, disponible))

        for reserva_datos in datos.get("reservas", []):
            cliente = self.buscar_cliente_por_documento(reserva_datos.get("cliente_documento"))
            habitacion = self.buscar_habitacion_por_numero(reserva_datos.get("habitacion_numero"))

            if cliente is not None and habitacion is not None:
                fecha_entrada = date.fromisoformat(reserva_datos.get("fecha_entrada"))
                fecha_salida = date.fromisoformat(reserva_datos.get("fecha_salida"))
                estado = reserva_datos.get("estado", "pendiente")
                self.agregar_reserva(Reserva(cliente, habitacion, fecha_entrada, fecha_salida, estado))

        if not self.habitaciones:
            self._crear_habitaciones_iniciales()

    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def agregar_reserva(self, reserva):
        self.reservas.append(reserva)

    def buscar_habitacion_por_numero(self, numero):
        for habitacion in self.habitaciones:
            if habitacion.numero == numero:
                return habitacion
        return None

    def buscar_cliente_por_documento(self, documento):
        for cliente in self.clientes:
            if cliente.documento == documento:
                return cliente
        return None

    def listar_habitaciones(self):
        if not self.habitaciones:
            print("No hay habitaciones registradas.")
            return

        print("\nHABITACIONES:")
        for habitacion in self.habitaciones:
            habitacion.mostrar_informacion()
            print("-")

    def listar_clientes(self):
        if not self.clientes:
            print("No hay clientes registrados.")
            return

        print("\nCLIENTES:")
        for cliente in self.clientes:
            cliente.mostrar_datos()
            print("-")

    def listar_reservas(self):
        if not self.reservas:
            print("No hay reservas realizadas.")
            return

        print("\nRESERVAS:")
        for reserva in self.reservas:
            reserva.mostrar_reserva()
            print("-")

    def habitacion_disponible(self, numero):
        habitacion = self.buscar_habitacion_por_numero(numero)
        if habitacion is None:
            return False
        return habitacion.disponible


class Habitacion:
    def __init__(self, numero, precio_por_noche, capacidad, disponible):
        self.numero = numero
        self.precio_por_noche = precio_por_noche
        self.capacidad = capacidad
        self.disponible = disponible

    def calcular_precio(self):
        return self.precio_por_noche

    def mostrar_informacion(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        print(f"Habitación {self.numero} | Capacidad: {self.capacidad} | Precio: ${self.precio_por_noche:.2f} | Estado: {estado}")


class HabitacionEstandar(Habitacion):
    def __init__(self, numero, precio_por_noche, capacidad, disponible):
        super().__init__(numero, precio_por_noche, capacidad, disponible)

    def calcular_precio(self):
        return self.precio_por_noche

    def mostrar_informacion(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        print(f"Habitación Estándar {self.numero} | Capacidad: {self.capacidad} | Precio: ${self.calcular_precio():.2f} | Estado: {estado}")


class Suite(Habitacion):
    def __init__(self, numero, precio_por_noche, capacidad, disponible, costo_extra):
        super().__init__(numero, precio_por_noche, capacidad, disponible)
        self.costo_extra = costo_extra

    def calcular_precio(self):
        return self.precio_por_noche + self.costo_extra

    def mostrar_informacion(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        print(f"Suite {self.numero} | Capacidad: {self.capacidad} | Precio: ${self.calcular_precio():.2f} | Estado: {estado}")


class HabitacionFamiliar(Habitacion):
    def __init__(self, numero, precio_por_noche, capacidad, disponible, aumento_familiar):
        super().__init__(numero, precio_por_noche, capacidad, disponible)
        self.aumento_familiar = aumento_familiar

    def calcular_precio(self):
        return self.precio_por_noche + self.aumento_familiar

    def mostrar_informacion(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        print(f"Habitación Familiar {self.numero} | Capacidad: {self.capacidad} | Precio: ${self.calcular_precio():.2f} | Estado: {estado}")


class Cliente:
    def __init__(self, nombre, documento, telefono):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono

    def mostrar_datos(self):
        print(f"Cliente: {self.nombre} | Documento: {self.documento} | Teléfono: {self.telefono}")


class Reserva:
    def __init__(self, cliente, habitacion, fecha_entrada, fecha_salida, estado="pendiente"):
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.estado = estado

    def calcular_total(self):
        noches = (self.fecha_salida - self.fecha_entrada).days
        return noches * self.habitacion.calcular_precio()

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def mostrar_reserva(self):
        total = self.calcular_total()
        print(f"Cliente: {self.cliente.nombre} | Habitación: {self.habitacion.numero} | Entrada: {self.fecha_entrada} | Salida: {self.fecha_salida} | Estado: {self.estado} | Total: ${total:.2f}")


def registrar_cliente(hotel):
    nombre = input("Nombre del cliente: ")
    documento = input("Documento: ")
    telefono = input("Teléfono: ")

    cliente = Cliente(nombre, documento, telefono)
    hotel.agregar_cliente(cliente)
    hotel.guardar_datos()
    print("Cliente registrado correctamente.")


def crear_reserva(hotel):
    documento = input("Ingrese el documento del cliente: ")
    cliente = hotel.buscar_cliente_por_documento(documento)

    if cliente is None:
        print("Cliente no encontrado.")
        return

    try:
        numero_habitacion = int(input("Ingrese el número de la habitación: "))
    except ValueError:
        print("Número de habitación inválido. Debe ingresar solo números.")
        return

    habitacion = hotel.buscar_habitacion_por_numero(numero_habitacion)

    if habitacion is None:
        print("Habitación no encontrada.")
        return

    if not hotel.habitacion_disponible(numero_habitacion):
        print("La habitación no está disponible.")
        return

    fecha_entrada = input("Fecha de entrada (YYYY-MM-DD): ")
    fecha_salida = input("Fecha de salida (YYYY-MM-DD): ")

    try:
        entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d").date()
        salida = datetime.strptime(fecha_salida, "%Y-%m-%d").date()
    except ValueError:
        print("Formato de fecha incorrecto. Use YYYY-MM-DD.")
        return

    if salida <= entrada:
        print("La fecha de salida debe ser posterior a la fecha de entrada.")
        return

    reserva = Reserva(cliente, habitacion, entrada, salida, "pendiente")
    total = reserva.calcular_total()

    habitacion.disponible = False
    hotel.agregar_reserva(reserva)
    hotel.guardar_datos()

    print(f"Reserva creada correctamente. Total estimado: ${total:.2f}")


def mostrar_menu():
    print("\n========================================")
    print("             SISTEMA DEL HOTEL")
    print("========================================")
    print("1. Registrar cliente")
    print("2. Ver habitaciones")
    print("3. Crear reserva")
    print("4. Ver reservas")
    print("5. Salir")
    print("========================================")


def main():
    hotel = Hotel("Hotel Principiante")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_cliente(hotel)
        elif opcion == "2":
            hotel.listar_habitaciones()
        elif opcion == "3":
            crear_reserva(hotel)
        elif opcion == "4":
            hotel.listar_reservas()
        elif opcion == "5":
            hotel.guardar_datos()
            print("Gracias por usar el sistema del hotel.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
