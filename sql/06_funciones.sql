USE Proyecto1_Transportes_SA;
GO

/* =========================================================
   FUNCIÓN 1: Asientos disponibles por viaje, devuelve cantidad disponible
   ========================================================= */
IF OBJECT_ID('dbo.fn_asientos_disponibles', 'FN') IS NOT NULL
    DROP FUNCTION dbo.fn_asientos_disponibles;
GO

CREATE FUNCTION dbo.fn_asientos_disponibles (@id_viaje INT)
RETURNS INT
AS
BEGIN
    DECLARE @cupo_total INT = 0;
    DECLARE @reservados INT = 0;
    DECLARE @disponibles INT;

    SELECT @cupo_total = cupo_total
    FROM dbo.VIAJES
    WHERE id_viaje = @id_viaje;

    SELECT @reservados = ISNULL(SUM(cantidad_pasajeros), 0)
    FROM dbo.RESERVACIONES
    WHERE id_viaje = @id_viaje
      AND id_estado NOT IN (
            SELECT id_estado
            FROM dbo.ESTADO_RESERVACION
            WHERE estado IN ('Cancelada', 'Vencida', 'NoShow')
      );

    SET @disponibles = ISNULL(@cupo_total, 0) - ISNULL(@reservados, 0);

    IF @disponibles < 0
        SET @disponibles = 0;

    RETURN @disponibles;
END;
GO

/* =========================================================
   FUNCIÓN 2: Tipo de cliente según rango salarial, recibe id_rango_salarial
   ========================================================= */
IF OBJECT_ID('dbo.fn_tipo_cliente', 'FN') IS NOT NULL
    DROP FUNCTION dbo.fn_tipo_cliente;
GO

CREATE FUNCTION dbo.fn_tipo_cliente (@id_rango_salarial INT)
RETURNS VARCHAR(20)
AS
BEGIN
    DECLARE @salario_max DECIMAL(10,2);
    DECLARE @tipo_cliente VARCHAR(20);

    SELECT @salario_max = salario_max
    FROM dbo.RANGOS_SALARIALES
    WHERE id_rango_salarial = @id_rango_salarial;

    SET @tipo_cliente = CASE
        WHEN @salario_max IS NULL THEN 'No definido'
        WHEN @salario_max >= 2000000 THEN 'VIP'
        WHEN @salario_max >= 800000 THEN 'Regular'
        ELSE 'Económico'
    END;

    RETURN @tipo_cliente;
END;
GO

/* =========================================================
   luego de ejecutar, podemos hacer estas pruebas, solo para visualizar datos.
   ========================================================= */
SELECT id_viaje, cupo_total
FROM VIAJES;

SELECT dbo.fn_asientos_disponibles(1) AS asientos_disponibles;

/*Insert de datos */

INSERT INTO RESERVACIONES
(id_reservacion, id_cliente, id_viaje, id_administrativo, fecha_reservacion, cantidad_pasajeros, subtotal, impuestos, total, id_estado)
SELECT 
    MAX(id_reservacion) + 1,
    1, 1, 1, GETDATE(), 3, 30000, 3900, 33900, 1
FROM RESERVACIONES;


/*consulta*/
SELECT *
FROM RESERVACIONES
WHERE id_viaje = 1;

/*Consulta de cupo*/
SELECT id_viaje, cupo_total
FROM VIAJES
WHERE id_viaje = 1;