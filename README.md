# Sistema de reservas de hotel

Este proyecto es un ejercicio sencillo de Programación Orientada a Objetos en Python. Consiste en un sistema para gestionar clientes, habitaciones y reservas de un hotel.

## Funcionalidades

- Registrar clientes
- Ver habitaciones
- Crear reservas
- Mostrar reservas
- Guardar y cargar datos con JSON

## Clases principales

- Hotel
- Habitacion
- HabitacionEstandar
- Suite
- HabitacionFamiliar
- Cliente
- Reserva

## POO aplicada

Se usan estos conceptos:
- Clases y objetos
- Atributos y métodos
- Herencia
- Polimorfismo

La clase base Habitacion tiene un método calcular_precio(), y cada clase hija lo define de manera diferente.

## Guardado de datos

Los datos se guardan en un archivo JSON llamado hotel_data.json. Allí se almacenan los clientes, las habitaciones y las reservas para que no se pierdan al cerrar el programa.

## Cómo ejecutar

```bash
python3 sistema_hotel.py
```
