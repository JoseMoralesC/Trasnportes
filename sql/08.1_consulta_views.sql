USE Proyecto1_Transportes_SA;
GO

/* =========================================================
   VALIDACION DE VISTAS
   Ejecutar después de: 08_views.sql
   ========================================================= */

PRINT '===== VALIDACION DE VISTAS =====';
GO

/* =========================================================
   1) CONSULTA GENERAL - VIEW RESERVACIONES
   ========================================================= */
PRINT '===== VIEW: vw_reservaciones_completas =====';

SELECT TOP 10 *
FROM dbo.vw_reservaciones_completas
ORDER BY id_reservacion DESC;
GO

/* =========================================================
   2) CONSULTA GENERAL - VIEW FACTURACION
   ========================================================= */
PRINT '===== VIEW: vw_facturacion_completa =====';

SELECT TOP 10 *
FROM dbo.vw_facturacion_completa
ORDER BY id_factura DESC;
GO

/* =========================================================
   3) VALIDACION POR RESERVACION ESPECIFICA
   ========================================================= */
PRINT '===== VALIDACION POR RESERVACION =====';

SELECT *
FROM dbo.vw_reservaciones_completas
WHERE id_reservacion = (
    SELECT MAX(id_reservacion)
    FROM dbo.RESERVACIONES
);
GO

/* =========================================================
   4) VALIDACION POR FACTURA ESPECIFICA
   ========================================================= */
PRINT '===== VALIDACION POR FACTURA =====';

SELECT *
FROM dbo.vw_facturacion_completa
WHERE id_factura = (
    SELECT MAX(id_factura)
    FROM dbo.FACTURAS
);
GO

/* =========================================================
   5) FILTRO POR CLIENTE
   ========================================================= */
PRINT '===== FILTRO POR CLIENTE =====';

SELECT TOP 10
    id_reservacion,
    cliente,
    correo,
    origen,
    destino,
    fecha_salida,
    cantidad_pasajeros,
    total,
    estado_reservacion
FROM dbo.vw_reservaciones_completas
WHERE cliente LIKE '%a%'
ORDER BY id_reservacion DESC;
GO

/* =========================================================
   6) FILTRO POR ESTADO DE RESERVACION
   ========================================================= */
PRINT '===== FILTRO POR ESTADO DE RESERVACION =====';

SELECT TOP 10
    id_reservacion,
    cliente,
    origen,
    destino,
    fecha_salida,
    total,
    estado_reservacion
FROM dbo.vw_reservaciones_completas
WHERE estado_reservacion IS NOT NULL
ORDER BY id_reservacion DESC;
GO

/* =========================================================
   7) FILTRO POR ESTADO DE FACTURA
   ========================================================= */
PRINT '===== FILTRO POR ESTADO DE FACTURA =====';

SELECT TOP 10
    id_factura,
    numero_factura,
    cliente,
    fecha_factura,
    subtotal,
    impuesto,
    descuento,
    total,
    estado_factura
FROM dbo.vw_facturacion_completa
WHERE estado_factura IS NOT NULL
ORDER BY id_factura DESC;
GO

/* =========================================================
   8) FACTURAS SIN DESCUENTO
   ========================================================= */
PRINT '===== FACTURAS SIN DESCUENTO =====';

SELECT TOP 10
    id_factura,
    numero_factura,
    cliente,
    fecha_factura,
    subtotal,
    impuesto,
    descuento,
    total
FROM dbo.vw_facturacion_completa
WHERE descuento = 'Sin dto'
ORDER BY id_factura DESC;
GO

/* =========================================================
   9) CONSULTA RESUMEN DE RESERVACIONES
   ========================================================= */
PRINT '===== RESUMEN DE RESERVACIONES =====';

SELECT
    estado_reservacion,
    COUNT(*) AS cantidad_reservaciones,
    SUM(total) AS monto_total
FROM dbo.vw_reservaciones_completas
GROUP BY estado_reservacion
ORDER BY estado_reservacion;
GO

/* =========================================================
   10) CONSULTA RESUMEN DE FACTURAS
   ========================================================= */
PRINT '===== RESUMEN DE FACTURAS =====';

SELECT
    estado_factura,
    COUNT(*) AS cantidad_facturas,
    SUM(total) AS monto_total_facturado
FROM dbo.vw_facturacion_completa
GROUP BY estado_factura
ORDER BY estado_factura;
GO