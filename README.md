#  Proyecto Transportes

Sistema de gestión de transportes desarrollado en Python con interfaz gráfica (Tkinter) y conexión a base de datos SQL Server.

---

##  Descripción General

Este sistema permite administrar de forma integral una operación de transporte, incluyendo:

- Gestión de autobuses
- Gestión de viajes
- Reservaciones de pasajeros
- Facturación
- Pagos
- Control de estados y catálogos

El sistema está construido siguiendo una arquitectura modular por capas, lo que facilita su mantenimiento, escalabilidad y reutilización.

---

##  Arquitectura del Proyecto

El proyecto está organizado en capas claramente definidas:

proyecto_transportes/
│
├── app.py
│
├── config/
│ ├── settings.py
│ └── database.py
│
├── core/
│ ├── db_manager.py
│ ├── logger.py
│ ├── exceptions.py
│ └── helpers.py
│
├── repositories/
│ ├── *_repository.py
│
├── services/
│ ├── *_service.py
│
├── ui/
│ ├── main_window.py
│ ├── módulos (autobuses, viajes, reservaciones, pagos, facturas)
│


---

##  Tecnologías Utilizadas

- Python 3
- Tkinter (Interfaz gráfica)
- ttk (estilos UI)
- tkcalendar (selector de fechas)
- SQL Server Express
- pyodbc (conexión a base de datos)

---

##  Arquitectura por Capas

###  UI (Presentación)
- Construida con Tkinter
- Maneja eventos del usuario
- No contiene lógica de negocio

###  Services (Lógica de negocio)
- Validaciones
- Reglas del sistema
- Coordinación entre UI y repositorios

###  Repositories (Acceso a datos)
- Consultas SQL
- Inserciones, actualizaciones y eliminaciones

###  Core
- Manejo de base de datos (`db_manager`)
- Logger centralizado
- Helpers reutilizables
- Manejo de excepciones

###  Config
- Configuración de conexión a base de datos
- Variables del sistema

---

##  Funcionalidades Principales

###  Autobuses
- Registro de unidades
- Control de número de unidad autogenerado
- Información de marca, modelo y año
- Control de DEKRA y marchamo

###  Viajes
- Creación de viajes
- Asignación de rutas, autobuses y precios
- Manejo de fechas con calendario

###  Reservaciones
- Registro de pasajeros
- Asociación a viajes
- Validaciones de disponibilidad

###  Facturación
- Generación automática de número de factura
- Relación con reservaciones

###  Pagos
- Registro de pagos
- Métodos de pago
- Estados de pago
- Asociación con facturas

---

##  Manejo de Fechas

El sistema utiliza `tkcalendar.DateEntry` para:

- Evitar ingreso manual incorrecto
- Mejorar experiencia de usuario
- Estandarizar formatos de fecha

---

##  Logs

El sistema implementa un logger centralizado:

- Registro de errores
- Registro de eventos importantes
- Facilita debugging y mantenimiento

---

## Buenas Prácticas Implementadas

- Separación de responsabilidades
- Validaciones en capa de servicios
- Manejo de errores controlado
- Código modular y reutilizable
- Tipado con `typing`

---

Autor

José Rodolfo Morales Calderón

Proyecto disponible en el repositorio de Github:
[Publico](https://github.com/JoseMoralesC/Trasnportes.git)