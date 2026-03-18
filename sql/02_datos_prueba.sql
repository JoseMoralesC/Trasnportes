/* =========================================================
   PROYECTO 1 - MODELO RELACIONAL
   Script de carga inicial de datos de prueba
   SQL Server / SSMS
   Base de datos: Proyecto1_Transportes
   ========================================================= */

USE Proyecto1_Transportes;
GO

/* =========================================================
   1. CATÁLOGOS BASE
   ========================================================= */

INSERT INTO PROFESIONES (id_profesion, nombre_profesion) VALUES
(1, 'Estudiante'),
(2, 'Docente'),
(3, 'Ingeniero');
GO

INSERT INTO EMPRESAS (id_empresa, nombre_empresa, telefono, direccion) VALUES
(1, 'Colegio Universitario', '2550-0001', 'Cartago Centro'),
(2, 'Tech Solutions CR', '2222-3344', 'San Jose'),
(3, 'Servicios del Este', '2551-8899', 'Tres Rios');
GO

INSERT INTO RANGOS_SALARIALES (id_rango_salarial, descripcion_rango, salario_min, salario_max) VALUES
(1, 'Bajo', 350000.00, 599999.99),
(2, 'Medio', 600000.00, 999999.99),
(3, 'Alto', 1000000.00, 2500000.00);
GO

INSERT INTO ROLES_EMPLEADO (id_rol, nombre_rol) VALUES
(1, 'Administrador'),
(2, 'Chofer'),
(3, 'Asistente');
GO

INSERT INTO LICENCIAS_CONDUCIR (id_licencia, tipo_licencia, descripcion) VALUES
(1, 'B1', 'Licencia liviana'),
(2, 'C2', 'Licencia autobus'),
(3, 'C3', 'Licencia transporte pesado');
GO

INSERT INTO ZONAS (id_zona, nombre_zona) VALUES
(1, 'Cartago'),
(2, 'San Jose'),
(3, 'Heredia');
GO

INSERT INTO PRECIO_BASE (id_precio, precio_base) VALUES
(1, 8500.00),
(2, 12000.00),
(3, 15000.00);
GO

INSERT INTO ESTADO_VIAJE (id_estado, estado) VALUES
(1, 'Activo'),
(2, 'Cancelado'),
(3, 'Finalizado');
GO

INSERT INTO NUMERO_UNIDAD (id_num_unidad, unidad) VALUES
(1, 'U-001'),
(2, 'U-002'),
(3, 'U-003');
GO

INSERT INTO MARCA_UNIDAD (id_marca, marca) VALUES
(1, 'Mercedes'),
(2, 'Hyundai'),
(3, 'Volvo');
GO

INSERT INTO MODELO_UNIDAD (id_modelo, modelo) VALUES
(1, '2020'),
(2, '2021'),
(3, '2022');
GO

INSERT INTO ESTADO_UNIDAD (id_estado, estado) VALUES
(1, 'Activo'),
(2, 'Taller'),
(3, 'Inactivo');
GO

INSERT INTO TIPOS_AUTOBUS (id_tipo_autobus, nombre_tipo, capacidad_pasajeros, descripcion) VALUES
(1, 'Microbus', 20, 'Unidad pequena para grupos cortos'),
(2, 'Regular', 40, 'Autobus de capacidad media'),
(3, 'Ejecutivo', 50, 'Autobus comodo para viajes largos');
GO

INSERT INTO ESTADO_DEKRA (id_estado, estado) VALUES
(1, 'Vigente'),
(2, 'Vencido');
GO

INSERT INTO ESTADO_MARCHAMO (id_estado, estado) VALUES
(1, 'Vigente'),
(2, 'Vencido');
GO

INSERT INTO ESTADO_RESERVACION (id_estado, estado) VALUES
(1, 'Activa'),
(2, 'Anulada'),
(3, 'Pagada');
GO

INSERT INTO DESCUENTOS (id_descuento, tipo_descuento) VALUES
(1, 'Adulto Mayor'),
(2, 'Promocion'),
(3, 'Estudiante');
GO

INSERT INTO ESTADO_FACTURA (id_estado, estado) VALUES
(1, 'Activa'),
(2, 'Nula'),
(3, 'Pagada');
GO

INSERT INTO METODOS_PAGO (id_metodo_pago, nombre_metodo) VALUES
(1, 'Efectivo'),
(2, 'Tarjeta'),
(3, 'Transferencia');
GO

INSERT INTO ESTADO_PAGO (id_estado, estado) VALUES
(1, 'Aplicado'),
(2, 'Pendiente'),
(3, 'Rechazado');
GO

/* =========================================================
   2. TABLAS CON DEPENDENCIAS
   ========================================================= */

INSERT INTO CLIENTES (
    id_cliente, cedula, nombre, apellido1, apellido2,
    id_profesion, id_empresa, id_rango_salarial,
    telefono, correo, direccion
) VALUES
(1, '305000192', 'Jose', 'Morales', 'Calderon', 1, 1, 1, '8888-1111', 'jose@email.com', 'Cartago'),
(2, '204560321', 'Maria', 'Rojas', 'Vega', 2, 2, 2, '8888-2222', 'maria@email.com', 'San Jose'),
(3, '109870654', 'Carlos', 'Mora', 'Jimenez', 3, 3, 3, '8888-3333', 'carlos@email.com', 'Heredia');
GO

INSERT INTO EMPLEADOS (
    id_empleado, cedula, nombre, apellido1, apellido2,
    telefono, correo, fecha_ingreso, id_rol, id_licencia
) VALUES
(1, '111111111', 'Laura', 'Sanchez', 'Lopez', '7000-1000', 'laura@empresa.com', '2025-01-10', 1, NULL),
(2, '222222222', 'Pedro', 'Ramirez', 'Castro', '7000-2000', 'pedro@empresa.com', '2025-01-15', 2, 2),
(3, '333333333', 'Ana', 'Vargas', 'Mendez', '7000-3000', 'ana@empresa.com', '2025-02-01', 3, NULL);
GO

INSERT INTO RUTAS (
    id_ruta, nombre_ruta, origen, destino,
    distancia_km, duracion_estimada, id_zona
) VALUES
(1, 'Cartago-San Jose', 'Cartago', 'San Jose', 25.50, '00:45', 1),
(2, 'San Jose-Heredia', 'San Jose', 'Heredia', 18.75, '00:35', 2),
(3, 'Cartago-Heredia', 'Cartago', 'Heredia', 40.20, '01:10', 3);
GO

INSERT INTO AUTOBUSES (
    id_autobus, placa, id_num_unidad, id_marca, id_modelo,
    anio, capacidad, id_estado, id_tipo_autobus
) VALUES
(1, 'ABC-101', 1, 1, 1, 2020, 20, 1, 1),
(2, 'DEF-202', 2, 2, 2, 2021, 40, 1, 2),
(3, 'GHI-303', 3, 3, 3, 2022, 50, 1, 3);
GO

INSERT INTO DEKRAS (
    id_dekra, id_autobus, numero_dekra,
    fecha_emision, fecha_vencimiento, id_estado
) VALUES
(1, 1, 'DK-0001', '2025-01-01', '2026-01-01', 1),
(2, 2, 'DK-0002', '2025-02-01', '2026-02-01', 1),
(3, 3, 'DK-0003', '2025-03-01', '2026-03-01', 1);
GO

INSERT INTO MARCHAMOS (
    id_marchamo, id_autobus, numero_marchamo,
    periodo, fecha_pago, fecha_vencimiento, id_estado
) VALUES
(1, 1, 'MC-2025-001', '2025', '2025-01-05', '2025-12-31', 1),
(2, 2, 'MC-2025-002', '2025', '2025-01-06', '2025-12-31', 1),
(3, 3, 'MC-2025-003', '2025', '2025-01-07', '2025-12-31', 1);
GO

INSERT INTO MANTENIMIENTOS_AUTOBUS (
    id_mantenimiento, id_autobus, tipo_mantenimiento,
    descripcion, fecha_mantenimiento, costo, taller
) VALUES
(1, 1, 'Preventivo', 'Cambio de aceite y revision general', '2025-02-10', 85000.00, 'Taller Cartago'),
(2, 2, 'Correctivo', 'Cambio de frenos delanteros', '2025-02-18', 125000.00, 'Taller San Jose'),
(3, 3, 'Preventivo', 'Revision de suspension', '2025-03-01', 95000.00, 'Taller Heredia');
GO

INSERT INTO VIAJES (
    id_viaje, id_ruta, id_autobus, fecha_salida,
    hora_salida, id_precio, cupo_total, id_estado
) VALUES
(1, 1, 1, '2026-03-20', '08:00:00', 1, 20, 1),
(2, 2, 2, '2026-03-21', '09:30:00', 2, 40, 1),
(3, 3, 3, '2026-03-22', '07:15:00', 3, 50, 1);
GO

INSERT INTO VIAJE_PERSONAL (
    id_viaje_personal, id_viaje, id_empleado, funcion_en_viaje
) VALUES
(1, 1, 2, 'Chofer'),
(2, 1, 3, 'Apoyo'),
(3, 2, 2, 'Chofer'),
(4, 3, 2, 'Chofer');
GO

INSERT INTO RESERVACIONES (
    id_reservacion, id_cliente, id_viaje, id_administrativo,
    fecha_reservacion, cantidad_pasajeros, subtotal, impuestos, total, id_estado
) VALUES
(1, 1, 1, 1, '2026-03-17', 2, 17000.00, 2210.00, 19210.00, 3),
(2, 2, 2, 1, '2026-03-17', 1, 12000.00, 1560.00, 13560.00, 1),
(3, 3, 3, 1, '2026-03-17', 3, 45000.00, 5850.00, 50850.00, 1);
GO

INSERT INTO DETALLE_RESERVACION (
    id_detalle_reservacion, id_reservacion, nombre_pasajero,
    apellido_pasajero, identificacion_pasajero, asiento, observaciones
) VALUES
(1, 1, 'Jose', 'Morales', '305000192', 'A1', 'Sin observaciones'),
(2, 1, 'Luis', 'Calderon', '305000193', 'A2', 'Sin observaciones'),
(3, 2, 'Maria', 'Rojas', '204560321', 'B1', 'Equipaje pequeno'),
(4, 3, 'Carlos', 'Mora', '109870654', 'C1', 'Sin observaciones'),
(5, 3, 'Elena', 'Jimenez', '109870655', 'C2', 'Sin observaciones'),
(6, 3, 'Pablo', 'Jimenez', '109870656', 'C3', 'Viaja con adulto');
GO

INSERT INTO FACTURAS (
    id_factura, id_reservacion, numero_factura, fecha_factura,
    subtotal, impuesto, id_descuento, total, id_estado
) VALUES
(1, 1, 'FAC-0001', '2026-03-17', 17000.00, 2210.00, NULL, 19210.00, 3),
(2, 2, 'FAC-0002', '2026-03-17', 12000.00, 1560.00, 2, 13560.00, 1),
(3, 3, 'FAC-0003', '2026-03-17', 45000.00, 5850.00, 3, 50850.00, 1);
GO

INSERT INTO PAGOS (
    id_pago, id_factura, id_metodo_pago, fecha_pago,
    monto_pagado, referencia_pago, id_estado
) VALUES
(1, 1, 2, '2026-03-17', 19210.00, 'REF-TARJ-0001', 1),
(2, 2, 1, '2026-03-17', 13560.00, 'REF-EFEC-0002', 2),
(3, 3, 3, '2026-03-17', 50850.00, 'REF-TRANS-0003', 2);
GO

INSERT INTO BITACORA (
    id_bitacora, id_empleado, fecha_hora,
    accion, tabla_afectada, id_registro_afectado, descripcion_evento
) VALUES
(1, 1, '2026-03-17 19:00:00', 'INSERT', 'CLIENTES', 1, 'Registro inicial de cliente Jose Morales'),
(2, 1, '2026-03-17 19:10:00', 'INSERT', 'RESERVACIONES', 1, 'Creacion de reservacion para viaje 1'),
(3, 1, '2026-03-17 19:15:00', 'INSERT', 'FACTURAS', 1, 'Generacion de factura FAC-0001');
GO