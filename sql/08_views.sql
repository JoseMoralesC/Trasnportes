USE Proyecto1_Transportes_SA;
GO

/* =========================================================
   VIEW 1: Reservaciones completas
   ========================================================= */
IF OBJECT_ID('dbo.vw_reservaciones_completas', 'V') IS NOT NULL
    DROP VIEW dbo.vw_reservaciones_completas;
GO

CREATE VIEW dbo.vw_reservaciones_completas
AS
SELECT
    r.id_reservacion,
    r.fecha_reservacion,
    c.id_cliente,
    CONCAT(c.nombre, ' ', c.apellido1, ' ', c.apellido2) AS cliente,
    c.correo,
    ru.origen,
    ru.destino,
    v.fecha_salida,
    v.hora_salida,
    a.placa AS autobus,
    CONCAT(e.nombre, ' ', e.apellido1, ' ', e.apellido2) AS administrativo,
    r.cantidad_pasajeros,
    r.subtotal,
    r.impuestos,
    r.total,
    er.estado AS estado_reservacion
FROM dbo.RESERVACIONES r
INNER JOIN dbo.CLIENTES c
    ON c.id_cliente = r.id_cliente
INNER JOIN dbo.VIAJES v
    ON v.id_viaje = r.id_viaje
INNER JOIN dbo.RUTAS ru
    ON ru.id_ruta = v.id_ruta
INNER JOIN dbo.AUTOBUSES a
    ON a.id_autobus = v.id_autobus
INNER JOIN dbo.EMPLEADOS e
    ON e.id_empleado = r.id_administrativo
INNER JOIN dbo.ESTADO_RESERVACION er
    ON er.id_estado = r.id_estado;
GO

/* =========================================================
   VIEW 2: Facturación completa
   ========================================================= */
IF OBJECT_ID('dbo.vw_facturacion_completa', 'V') IS NOT NULL
    DROP VIEW dbo.vw_facturacion_completa;
GO

CREATE VIEW dbo.vw_facturacion_completa
AS
SELECT
    f.id_factura,
    f.numero_factura,
    f.fecha_factura,
    r.id_reservacion,
    CONCAT(c.nombre, ' ', c.apellido1, ' ', c.apellido2) AS cliente,
    ru.origen,
    ru.destino,
    v.fecha_salida,
    f.subtotal,
    f.impuesto,
    ISNULL(d.tipo_descuento, 'Sin dto') AS descuento,
    f.total,
    ef.estado AS estado_factura,
    CONCAT(e.nombre, ' ', e.apellido1, ' ', e.apellido2) AS administrativo
FROM dbo.FACTURAS f
INNER JOIN dbo.RESERVACIONES r
    ON r.id_reservacion = f.id_reservacion
INNER JOIN dbo.CLIENTES c
    ON c.id_cliente = r.id_cliente
INNER JOIN dbo.VIAJES v
    ON v.id_viaje = r.id_viaje
INNER JOIN dbo.RUTAS ru
    ON ru.id_ruta = v.id_ruta
INNER JOIN dbo.EMPLEADOS e
    ON e.id_empleado = r.id_administrativo
LEFT JOIN dbo.DESCUENTOS d
    ON d.id_descuento = f.id_descuento
INNER JOIN dbo.ESTADO_FACTURA ef
    ON ef.id_estado = f.id_estado;
GO
