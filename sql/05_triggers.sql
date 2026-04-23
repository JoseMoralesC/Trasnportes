USE Proyecto1_Transportes_SA;
GO

/* =========================================================
   TRIGGER 1: Actualizar estado del autobús por mantenimiento
   Adaptación al modelo actual:
   - AFTER INSERT: pone el autobús en estado Mantto
   - AFTER UPDATE: si el mantenimiento se marca como FINALIZADO
     o TERMINADO en tipo/descripción, lo pasa a Disp
   ========================================================= */
IF OBJECT_ID('dbo.trg_mantenimiento_estado_autobus', 'TR') IS NOT NULL
    DROP TRIGGER dbo.trg_mantenimiento_estado_autobus;
GO

CREATE TRIGGER dbo.trg_mantenimiento_estado_autobus
ON dbo.MANTENIMIENTOS_AUTOBUS
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @estado_mantto INT;
    DECLARE @estado_disponible INT;

    SELECT @estado_mantto = id_estado
    FROM dbo.ESTADO_UNIDAD
    WHERE estado = 'Mantto';

    SELECT @estado_disponible = id_estado
    FROM dbo.ESTADO_UNIDAD
    WHERE estado = 'Disp';

    IF @estado_mantto IS NULL OR @estado_disponible IS NULL
    BEGIN
        RAISERROR('No existen los estados requeridos en ESTADO_UNIDAD (Mantto / Disp).', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END;

    UPDATE a
       SET a.id_estado = @estado_mantto
    FROM dbo.AUTOBUSES a
    INNER JOIN inserted i
        ON i.id_autobus = a.id_autobus
    WHERE UPPER(ISNULL(i.tipo_mantenimiento, '')) NOT LIKE '%FINALIZADO%'
      AND UPPER(ISNULL(i.tipo_mantenimiento, '')) NOT LIKE '%TERMINADO%'
      AND UPPER(ISNULL(i.descripcion, '')) NOT LIKE '%FINALIZADO%'
      AND UPPER(ISNULL(i.descripcion, '')) NOT LIKE '%TERMINADO%';

    /* Convención para cierre del mantenimiento mientras la tabla no tenga fecha_fin */
    UPDATE a
       SET a.id_estado = @estado_disponible
    FROM dbo.AUTOBUSES a
    INNER JOIN inserted i
        ON i.id_autobus = a.id_autobus
    WHERE UPPER(ISNULL(i.tipo_mantenimiento, '')) LIKE '%FINALIZADO%'
       OR UPPER(ISNULL(i.tipo_mantenimiento, '')) LIKE '%TERMINADO%'
       OR UPPER(ISNULL(i.descripcion, '')) LIKE '%FINALIZADO%'
       OR UPPER(ISNULL(i.descripcion, '')) LIKE '%TERMINADO%';
END;
GO

/* =========================================================
   TRIGGER 2: Auditoría automática sobre RESERVACIONES
   ========================================================= */
IF OBJECT_ID('dbo.trg_auditoria_reservaciones', 'TR') IS NOT NULL
    DROP TRIGGER dbo.trg_auditoria_reservaciones;
GO

CREATE TRIGGER dbo.trg_auditoria_reservaciones
ON dbo.RESERVACIONES
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @accion VARCHAR(10);

    SET @accion = CASE
        WHEN EXISTS (SELECT 1 FROM inserted) AND EXISTS (SELECT 1 FROM deleted) THEN 'UPDATE'
        WHEN EXISTS (SELECT 1 FROM inserted) THEN 'INSERT'
        ELSE 'DELETE'
    END;

    INSERT INTO dbo.BITACORA
    (
        id_bitacora,
        id_empleado,
        fecha_hora,
        accion,
        tabla_afectada,
        id_registro_afectado,
        descripcion_evento
    )
    SELECT
        ROW_NUMBER() OVER (ORDER BY x.id_registro_afectado)
        + ISNULL((SELECT MAX(id_bitacora) FROM dbo.BITACORA), 0),
        x.id_empleado,
        GETDATE(),
        @accion,
        'RESERVACIONES',
        x.id_registro_afectado,
        CONCAT('Auditoría automática sobre RESERVACIONES. Acción: ', @accion, ' - Registro ', x.id_registro_afectado)
    FROM
    (
        SELECT i.id_reservacion AS id_registro_afectado,
               ISNULL(i.id_administrativo, 1) AS id_empleado
        FROM inserted i
        UNION
        SELECT d.id_reservacion AS id_registro_afectado,
               ISNULL(d.id_administrativo, 1) AS id_empleado
        FROM deleted d
    ) x;
END;
GO

/* =========================================================
   TRIGGER 3: Auditoría automática sobre FACTURAS
   Nota: en SQL Server la auditoría de dos tablas distintas
   requiere dos triggers DML separados.
   ========================================================= */
IF OBJECT_ID('dbo.trg_auditoria_facturas', 'TR') IS NOT NULL
    DROP TRIGGER dbo.trg_auditoria_facturas;
GO

CREATE TRIGGER dbo.trg_auditoria_facturas
ON dbo.FACTURAS
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @accion VARCHAR(10);

    SET @accion = CASE
        WHEN EXISTS (SELECT 1 FROM inserted) AND EXISTS (SELECT 1 FROM deleted) THEN 'UPDATE'
        WHEN EXISTS (SELECT 1 FROM inserted) THEN 'INSERT'
        ELSE 'DELETE'
    END;

    INSERT INTO dbo.BITACORA
    (
        id_bitacora,
        id_empleado,
        fecha_hora,
        accion,
        tabla_afectada,
        id_registro_afectado,
        descripcion_evento
    )
    SELECT
        ROW_NUMBER() OVER (ORDER BY x.id_registro_afectado)
        + ISNULL((SELECT MAX(id_bitacora) FROM dbo.BITACORA), 0),
        x.id_empleado,
        GETDATE(),
        @accion,
        'FACTURAS',
        x.id_registro_afectado,
        CONCAT('Auditoría automática sobre FACTURAS. Acción: ', @accion, ' - Registro ', x.id_registro_afectado)
    FROM
    (
        SELECT i.id_factura AS id_registro_afectado,
               ISNULL(r.id_administrativo, 1) AS id_empleado
        FROM inserted i
        INNER JOIN dbo.RESERVACIONES r
            ON r.id_reservacion = i.id_reservacion
        UNION
        SELECT d.id_factura AS id_registro_afectado,
               ISNULL(r.id_administrativo, 1) AS id_empleado
        FROM deleted d
        INNER JOIN dbo.RESERVACIONES r
            ON r.id_reservacion = d.id_reservacion
    ) x;
END;
GO
