USE Proyecto1_Transportes_SA;
GO

/* =========================================================
   SP 1: Crear reservación completa
   - Valida disponibilidad
   - Asigna empleado administrativo automáticamente
   - Calcula costo base
   - Usa transacción
   ========================================================= */
IF OBJECT_ID('dbo.sp_crear_reservacion', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_crear_reservacion;
GO

CREATE PROCEDURE dbo.sp_crear_reservacion
    @id_cliente INT,
    @id_viaje INT,
    @cantidad_pasajeros INT,
    @fecha_reservacion DATE = NULL,
    @id_estado_reservacion INT = 1
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @id_reservacion INT;
    DECLARE @id_administrativo INT;
    DECLARE @precio_base DECIMAL(10,2);
    DECLARE @subtotal DECIMAL(10,2);
    DECLARE @impuestos DECIMAL(10,2);
    DECLARE @total DECIMAL(10,2);
    DECLARE @asientos_disponibles INT;

    BEGIN TRY
        BEGIN TRANSACTION;

        IF @fecha_reservacion IS NULL
            SET @fecha_reservacion = CAST(GETDATE() AS DATE);

        IF NOT EXISTS (SELECT 1 FROM dbo.CLIENTES WHERE id_cliente = @id_cliente)
            RAISERROR('El cliente indicado no existe.', 16, 1);

        IF NOT EXISTS (SELECT 1 FROM dbo.VIAJES WHERE id_viaje = @id_viaje)
            RAISERROR('El viaje indicado no existe.', 16, 1);

        IF @cantidad_pasajeros <= 0
            RAISERROR('La cantidad de pasajeros debe ser mayor a cero.', 16, 1);

        SELECT @asientos_disponibles = dbo.fn_asientos_disponibles(@id_viaje);

        IF @asientos_disponibles < @cantidad_pasajeros
            RAISERROR('No hay asientos disponibles suficientes para completar la reservación.', 16, 1);

        SELECT TOP (1) @id_administrativo = e.id_empleado
        FROM dbo.EMPLEADOS e
        INNER JOIN dbo.ROLES_EMPLEADO r
            ON r.id_rol = e.id_rol
        WHERE r.nombre_rol IN ('Admin', 'Cajero', 'CallCtr')
        ORDER BY e.id_empleado;

        IF @id_administrativo IS NULL
            RAISERROR('No existe un empleado administrativo disponible para asignar la reservación.', 16, 1);

        SELECT @precio_base = pb.precio_base
        FROM dbo.VIAJES v
        INNER JOIN dbo.PRECIO_BASE pb
            ON pb.id_precio = v.id_precio
        WHERE v.id_viaje = @id_viaje;

        IF @precio_base IS NULL
            RAISERROR('No se pudo obtener el precio base del viaje.', 16, 1);

        SET @subtotal = @precio_base * @cantidad_pasajeros;
        SET @impuestos = ROUND(@subtotal * 0.13, 2);
        SET @total = @subtotal + @impuestos;

        SELECT @id_reservacion = ISNULL(MAX(id_reservacion), 0) + 1
        FROM dbo.RESERVACIONES;

        INSERT INTO dbo.RESERVACIONES
        (
            id_reservacion,
            id_cliente,
            id_viaje,
            id_administrativo,
            fecha_reservacion,
            cantidad_pasajeros,
            subtotal,
            impuestos,
            total,
            id_estado
        )
        VALUES
        (
            @id_reservacion,
            @id_cliente,
            @id_viaje,
            @id_administrativo,
            @fecha_reservacion,
            @cantidad_pasajeros,
            @subtotal,
            @impuestos,
            @total,
            @id_estado_reservacion
        );

        COMMIT TRANSACTION;

        SELECT
            @id_reservacion AS id_reservacion_creada,
            @id_administrativo AS id_administrativo_asignado,
            @subtotal AS subtotal,
            @impuestos AS impuestos,
            @total AS total;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        THROW;
    END CATCH
END;
GO

/* =========================================================
   SP 2: Generar factura automáticamente
   ========================================================= */
IF OBJECT_ID('dbo.sp_generar_factura', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_generar_factura;
GO

CREATE PROCEDURE dbo.sp_generar_factura
    @id_reservacion INT,
    @id_descuento INT = NULL,
    @id_estado_factura INT = 1
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @id_factura INT;
    DECLARE @numero_factura VARCHAR(20);
    DECLARE @fecha_factura DATE = CAST(GETDATE() AS DATE);
    DECLARE @subtotal DECIMAL(10,2);
    DECLARE @impuesto DECIMAL(10,2);
    DECLARE @total_base DECIMAL(10,2);
    DECLARE @porcentaje_descuento DECIMAL(5,2) = 0;
    DECLARE @monto_descuento DECIMAL(10,2) = 0;
    DECLARE @total_final DECIMAL(10,2);

    BEGIN TRY
        BEGIN TRANSACTION;

        IF NOT EXISTS (SELECT 1 FROM dbo.RESERVACIONES WHERE id_reservacion = @id_reservacion)
            RAISERROR('La reservación indicada no existe.', 16, 1);

        IF EXISTS (SELECT 1 FROM dbo.FACTURAS WHERE id_reservacion = @id_reservacion)
            RAISERROR('La reservación ya tiene una factura asociada.', 16, 1);

        SELECT
            @subtotal = subtotal,
            @impuesto = impuestos,
            @total_base = total
        FROM dbo.RESERVACIONES
        WHERE id_reservacion = @id_reservacion;

        SET @porcentaje_descuento = CASE ISNULL(@id_descuento, 1)
            WHEN 1 THEN 0.00
            WHEN 2 THEN 0.10
            WHEN 3 THEN 0.08
            WHEN 4 THEN 0.05
            WHEN 5 THEN 0.07
            WHEN 6 THEN 0.12
            WHEN 7 THEN 0.09
            WHEN 8 THEN 0.15
            WHEN 9 THEN 0.06
            WHEN 10 THEN 0.10
            WHEN 11 THEN 0.04
            WHEN 12 THEN 0.05
            WHEN 13 THEN 0.06
            WHEN 14 THEN 0.07
            WHEN 15 THEN 0.12
            ELSE 0.00
        END;

        SET @monto_descuento = ROUND(@total_base * @porcentaje_descuento, 2);
        SET @total_final = @total_base - @monto_descuento;

        SELECT @id_factura = ISNULL(MAX(id_factura), 0) + 1
        FROM dbo.FACTURAS;

        SET @numero_factura = CONCAT('FAC-', YEAR(@fecha_factura), '-', RIGHT('0000' + CAST(@id_factura AS VARCHAR(10)), 4));

        INSERT INTO dbo.FACTURAS
        (
            id_factura,
            id_reservacion,
            numero_factura,
            fecha_factura,
            subtotal,
            impuesto,
            id_descuento,
            total,
            id_estado
        )
        VALUES
        (
            @id_factura,
            @id_reservacion,
            @numero_factura,
            @fecha_factura,
            @subtotal,
            @impuesto,
            @id_descuento,
            @total_final,
            @id_estado_factura
        );

        COMMIT TRANSACTION;

        SELECT
            @id_factura AS id_factura_generada,
            @numero_factura AS numero_factura,
            @subtotal AS subtotal,
            @impuesto AS impuesto,
            @monto_descuento AS monto_descuento,
            @total_final AS total_final;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        THROW;
    END CATCH
END;
GO

/* =========================================================
   SP 3: Asignar autobús y conductor a un viaje/ruta
   Adaptado al modelo real usando VIAJES + VIAJE_PERSONAL
   ========================================================= */
IF OBJECT_ID('dbo.sp_asignar_unidad_ruta', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_asignar_unidad_ruta;
GO

CREATE PROCEDURE dbo.sp_asignar_unidad_ruta
    @id_viaje INT,
    @id_autobus INT,
    @id_conductor INT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @fecha_salida DATE;
    DECLARE @hora_salida TIME;
    DECLARE @id_estado_asignado INT;
    DECLARE @id_viaje_personal INT;

    BEGIN TRY
        BEGIN TRANSACTION;

        IF NOT EXISTS (SELECT 1 FROM dbo.VIAJES WHERE id_viaje = @id_viaje)
            RAISERROR('El viaje indicado no existe.', 16, 1);

        IF NOT EXISTS (SELECT 1 FROM dbo.AUTOBUSES WHERE id_autobus = @id_autobus)
            RAISERROR('El autobús indicado no existe.', 16, 1);

        IF NOT EXISTS (SELECT 1 FROM dbo.EMPLEADOS WHERE id_empleado = @id_conductor)
            RAISERROR('El conductor indicado no existe.', 16, 1);

        IF EXISTS (
            SELECT 1
            FROM dbo.AUTOBUSES a
            INNER JOIN dbo.ESTADO_UNIDAD eu
                ON eu.id_estado = a.id_estado
            WHERE a.id_autobus = @id_autobus
              AND eu.estado NOT IN ('Disp', 'Listo', 'Activo', 'Opera')
        )
            RAISERROR('El autobús no se encuentra disponible para asignación.', 16, 1);

        SELECT
            @fecha_salida = fecha_salida,
            @hora_salida = hora_salida
        FROM dbo.VIAJES
        WHERE id_viaje = @id_viaje;

        IF EXISTS (
            SELECT 1
            FROM dbo.VIAJE_PERSONAL vp
            INNER JOIN dbo.VIAJES v
                ON v.id_viaje = vp.id_viaje
            WHERE vp.id_empleado = @id_conductor
              AND vp.funcion_en_viaje = 'Chofer'
              AND v.fecha_salida = @fecha_salida
              AND v.hora_salida = @hora_salida
              AND v.id_viaje <> @id_viaje
        )
            RAISERROR('El conductor ya tiene otro viaje asignado en la misma fecha y hora.', 16, 1);

        UPDATE dbo.VIAJES
           SET id_autobus = @id_autobus
        WHERE id_viaje = @id_viaje;

        IF EXISTS (
            SELECT 1
            FROM dbo.VIAJE_PERSONAL
            WHERE id_viaje = @id_viaje
              AND funcion_en_viaje = 'Chofer'
        )
        BEGIN
            UPDATE dbo.VIAJE_PERSONAL
               SET id_empleado = @id_conductor
            WHERE id_viaje = @id_viaje
              AND funcion_en_viaje = 'Chofer';
        END
        ELSE
        BEGIN
            SELECT @id_viaje_personal = ISNULL(MAX(id_viaje_personal), 0) + 1
            FROM dbo.VIAJE_PERSONAL;

            INSERT INTO dbo.VIAJE_PERSONAL
            (
                id_viaje_personal,
                id_viaje,
                id_empleado,
                funcion_en_viaje
            )
            VALUES
            (
                @id_viaje_personal,
                @id_viaje,
                @id_conductor,
                'Chofer'
            );
        END;

        SELECT @id_estado_asignado = id_estado
        FROM dbo.ESTADO_UNIDAD
        WHERE estado = 'Asign';

        IF @id_estado_asignado IS NOT NULL
        BEGIN
            UPDATE dbo.AUTOBUSES
               SET id_estado = @id_estado_asignado
            WHERE id_autobus = @id_autobus;
        END;

        COMMIT TRANSACTION;

        SELECT
            @id_viaje AS id_viaje,
            @id_autobus AS id_autobus_asignado,
            @id_conductor AS id_conductor_asignado,
            'Asignación realizada correctamente' AS resultado;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        THROW;
    END CATCH
END;
GO

/* =========================================================
   SP 4: Reporte de ingresos por período
   ========================================================= */
IF OBJECT_ID('dbo.sp_reporte_ingresos', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_reporte_ingresos;
GO

CREATE PROCEDURE dbo.sp_reporte_ingresos
    @fecha_inicio DATE,
    @fecha_fin DATE
AS
BEGIN
    SET NOCOUNT ON;

    IF @fecha_inicio IS NULL OR @fecha_fin IS NULL
    BEGIN
        RAISERROR('Debe indicar fecha_inicio y fecha_fin.', 16, 1);
        RETURN;
    END;

    IF @fecha_inicio > @fecha_fin
    BEGIN
        RAISERROR('La fecha_inicio no puede ser mayor que fecha_fin.', 16, 1);
        RETURN;
    END;

    SELECT
        @fecha_inicio AS fecha_inicio,
        @fecha_fin AS fecha_fin,
        ISNULL(SUM(f.total), 0) AS total_facturado,
        COUNT(DISTINCT v.id_viaje) AS cantidad_viajes,
        CASE
            WHEN COUNT(DISTINCT v.id_viaje) = 0 THEN 0
            ELSE CAST(SUM(f.total) / COUNT(DISTINCT v.id_viaje) AS DECIMAL(10,2))
        END AS promedio_por_viaje
    FROM dbo.FACTURAS f
    INNER JOIN dbo.RESERVACIONES r
        ON r.id_reservacion = f.id_reservacion
    INNER JOIN dbo.VIAJES v
        ON v.id_viaje = r.id_viaje
    WHERE f.fecha_factura BETWEEN @fecha_inicio AND @fecha_fin;
END;
GO


