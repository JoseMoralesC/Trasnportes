/* =========================================================
   VALIDACION DE STORED PROCEDURES
   Proyecto: Sistema de Gestión de Reservas de Viajes
   ========================================================= */

USE Proyecto1_Transportes_SA;
GO

/* =========================================================
   1) DATOS INICIALES DE REFERENCIA
   ========================================================= */

PRINT '===== DATOS BASE =====';

SELECT TOP 10 * FROM CLIENTES ORDER BY id_cliente;
SELECT TOP 10 * FROM VIAJES ORDER BY id_viaje;
SELECT TOP 10 * FROM EMPLEADOS ORDER BY id_empleado;
SELECT TOP 10 * FROM AUTOBUSES ORDER BY id_autobus;
SELECT TOP 10 * FROM VIAJE_PERSONAL ORDER BY id_viaje, id_empleado;
GO

/* =========================================================
   2) VALIDACION DE sp_crear_reservacion
   ========================================================= */

PRINT '===== ANTES DE sp_crear_reservacion =====';

SELECT MAX(id_reservacion) AS ultima_reservacion
FROM RESERVACIONES;

SELECT *
FROM RESERVACIONES
WHERE id_viaje = 1
ORDER BY id_reservacion DESC;

SELECT dbo.fn_asientos_disponibles(1) AS asientos_disponibles_antes;
GO

/* ---- EJECUTAR SP ---- */
EXEC sp_crear_reservacion
    @id_cliente = 1,
    @id_viaje = 1,
    @cantidad_pasajeros = 2;
GO

PRINT '===== DESPUES DE sp_crear_reservacion =====';

SELECT TOP 5 *
FROM RESERVACIONES
ORDER BY id_reservacion DESC;

SELECT dbo.fn_asientos_disponibles(1) AS asientos_disponibles_despues;
GO

/* =========================================================
   3) VALIDACION DE sp_generar_factura
   ========================================================= */

PRINT '===== ANTES DE sp_generar_factura =====';

SELECT MAX(id_factura) AS ultima_factura
FROM FACTURAS;

SELECT TOP 10 *
FROM FACTURAS
ORDER BY id_factura DESC;

SELECT TOP 1 id_reservacion
FROM RESERVACIONES
ORDER BY id_reservacion DESC;
GO

/* ---- EJECUTAR SP ----
   Toma la última reservación registrada.
*/
DECLARE @ultima_reservacion INT;

SELECT @ultima_reservacion = MAX(id_reservacion)
FROM RESERVACIONES;

EXEC sp_generar_factura
    @id_reservacion = @ultima_reservacion;
GO

PRINT '===== DESPUES DE sp_generar_factura =====';

SELECT TOP 5 *
FROM FACTURAS
ORDER BY id_factura DESC;
GO

/* =========================================================
   4) VALIDACION DE sp_asignar_unidad_ruta
   ========================================================= */

PRINT '===== ANTES DE sp_asignar_unidad_ruta =====';

SELECT id_viaje, id_autobus, id_estado
FROM VIAJES
WHERE id_viaje = 10;

SELECT *
FROM VIAJE_PERSONAL
WHERE id_viaje = 10;

SELECT id_autobus, id_estado
FROM AUTOBUSES
WHERE id_autobus = 10;
GO

/* ---- EJECUTAR SP ---- */
EXEC sp_asignar_unidad_ruta
    @id_viaje = 10,
    @id_autobus = 10,
    @id_conductor = 10;
GO

PRINT '===== DESPUES DE sp_asignar_unidad_ruta =====';

SELECT id_viaje, id_autobus, id_estado
FROM VIAJES
WHERE id_viaje = 10;

SELECT *
FROM VIAJE_PERSONAL
WHERE id_viaje = 10;

SELECT id_autobus, id_estado
FROM AUTOBUSES
WHERE id_autobus = 10;
GO

/* =========================================================
   5) VALIDACION DE sp_reporte_ingresos
   ========================================================= */

PRINT '===== VALIDACION DE sp_reporte_ingresos =====';

EXEC sp_reporte_ingresos
    @fecha_inicio = '2025-01-01',
    @fecha_fin = '2026-12-31';
GO

/* =========================================================
   6) CONSULTAS EXTRA DE APOYO
   ========================================================= */

PRINT '===== CONSULTAS EXTRA =====';

-- Reservaciones recientes
SELECT TOP 10
    r.id_reservacion,
    r.id_cliente,
    r.id_viaje,
    r.id_administrativo,
    r.fecha_reservacion,
    r.cantidad_pasajeros,
    r.subtotal,
    r.impuestos,
    r.total,
    r.id_estado
FROM RESERVACIONES r
ORDER BY r.id_reservacion DESC;

-- Facturas recientes
SELECT TOP 10
    f.id_factura,
    f.id_reservacion,
    f.numero_factura,
    f.fecha_factura,
    f.subtotal,
    f.impuesto,
    f.id_descuento,
    f.total,
    f.id_estado
FROM FACTURAS f
ORDER BY f.id_factura DESC;

-- Bitácora reciente
SELECT TOP 10 *
FROM BITACORA
ORDER BY fecha_hora DESC;
GO