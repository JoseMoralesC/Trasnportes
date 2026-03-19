/* =========================================================
   PROYECTO 1 - MODELO RELACIONAL
   Script de creación de base de datos
   SQL Server / SSMS
   ========================================================= */

IF DB_ID('Proyecto1_Transportes_SA') IS NOT NULL
BEGIN
    ALTER DATABASE Proyecto1_Transportes_SA SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE Proyecto1_Transportes_SA;
END;
GO

CREATE DATABASE Proyecto1_Transportes_SA;
GO

USE Proyecto1_Transportes_SA;
GO

/* =========================================================
   1. PROFESIONES
   ========================================================= */
CREATE TABLE PROFESIONES (
    id_profesion INT NOT NULL,
    nombre_profesion VARCHAR(20) NOT NULL,
    CONSTRAINT PK_PROFESIONES PRIMARY KEY (id_profesion)
);
GO

/* =========================================================
   2. EMPRESAS
   ========================================================= */
CREATE TABLE EMPRESAS (
    id_empresa INT NOT NULL,
    nombre_empresa VARCHAR(60) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    CONSTRAINT PK_EMPRESAS PRIMARY KEY (id_empresa)
);
GO

/* =========================================================
   3. RANGOS_SALARIALES
   ========================================================= */
CREATE TABLE RANGOS_SALARIALES (
    id_rango_salarial INT NOT NULL,
    descripcion_rango VARCHAR(30) NOT NULL,
    salario_min DECIMAL(10,2) NOT NULL,
    salario_max DECIMAL(10,2) NOT NULL,
    CONSTRAINT PK_RANGOS_SALARIALES PRIMARY KEY (id_rango_salarial)
);
GO

/* =========================================================
   4. CLIENTES
   ========================================================= */
CREATE TABLE CLIENTES (
    id_cliente INT NOT NULL,
    cedula VARCHAR(20) NOT NULL,
    nombre VARCHAR(25) NOT NULL,
    apellido1 VARCHAR(25) NOT NULL,
    apellido2 VARCHAR(25) NOT NULL,
    id_profesion INT NOT NULL,
    id_empresa INT NOT NULL,
    id_rango_salarial INT NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    CONSTRAINT PK_CLIENTES PRIMARY KEY (id_cliente),
    CONSTRAINT UQ_CLIENTES_CEDULA UNIQUE (cedula),
    CONSTRAINT UQ_CLIENTES_CORREO UNIQUE (correo),
    CONSTRAINT FK_CLIENTES_PROFESIONES FOREIGN KEY (id_profesion)
        REFERENCES PROFESIONES(id_profesion),
    CONSTRAINT FK_CLIENTES_EMPRESAS FOREIGN KEY (id_empresa)
        REFERENCES EMPRESAS(id_empresa),
    CONSTRAINT FK_CLIENTES_RANGOS_SALARIALES FOREIGN KEY (id_rango_salarial)
        REFERENCES RANGOS_SALARIALES(id_rango_salarial)
);
GO

/* =========================================================
   5. ROLES_EMPLEADO
   ========================================================= */
CREATE TABLE ROLES_EMPLEADO (
    id_rol INT NOT NULL,
    nombre_rol VARCHAR(30) NOT NULL,
    CONSTRAINT PK_ROLES_EMPLEADO PRIMARY KEY (id_rol),
    CONSTRAINT UQ_ROLES_EMPLEADO_NOMBRE_ROL UNIQUE (nombre_rol)
);
GO

/* =========================================================
   6. LICENCIAS_CONDUCIR
   ========================================================= */
CREATE TABLE LICENCIAS_CONDUCIR (
    id_licencia INT NOT NULL,
    tipo_licencia VARCHAR(10) NOT NULL,
    descripcion VARCHAR(50) NOT NULL,
    CONSTRAINT PK_LICENCIAS_CONDUCIR PRIMARY KEY (id_licencia),
    CONSTRAINT UQ_LICENCIAS_CONDUCIR_TIPO UNIQUE (tipo_licencia)
);
GO

/* =========================================================
   7. EMPLEADOS
   ========================================================= */
CREATE TABLE EMPLEADOS (
    id_empleado INT NOT NULL,
    cedula VARCHAR(20) NOT NULL,
    nombre VARCHAR(25) NOT NULL,
    apellido1 VARCHAR(25) NOT NULL,
    apellido2 VARCHAR(25) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    id_rol INT NOT NULL,
    id_licencia INT NULL,
    CONSTRAINT PK_EMPLEADOS PRIMARY KEY (id_empleado),
    CONSTRAINT UQ_EMPLEADOS_CEDULA UNIQUE (cedula),
    CONSTRAINT UQ_EMPLEADOS_CORREO UNIQUE (correo),
    CONSTRAINT FK_EMPLEADOS_ROLES_EMPLEADO FOREIGN KEY (id_rol)
        REFERENCES ROLES_EMPLEADO(id_rol),
    CONSTRAINT FK_EMPLEADOS_LICENCIAS_CONDUCIR FOREIGN KEY (id_licencia)
        REFERENCES LICENCIAS_CONDUCIR(id_licencia)
);
GO

/* =========================================================
   8. ZONAS
   ========================================================= */
CREATE TABLE ZONAS (
    id_zona INT NOT NULL,
    nombre_zona VARCHAR(40) NOT NULL,
    CONSTRAINT PK_ZONAS PRIMARY KEY (id_zona),
    CONSTRAINT UQ_ZONAS_NOMBRE_ZONA UNIQUE (nombre_zona)
);
GO

/* =========================================================
   9. RUTAS
   ========================================================= */
CREATE TABLE RUTAS (
    id_ruta INT NOT NULL,
    nombre_ruta VARCHAR(50) NOT NULL,
    origen VARCHAR(50) NOT NULL,
    destino VARCHAR(50) NOT NULL,
    distancia_km DECIMAL(10,2) NOT NULL,
    duracion_estimada VARCHAR(20) NOT NULL,
    id_zona INT NOT NULL,
    CONSTRAINT PK_RUTAS PRIMARY KEY (id_ruta),
    CONSTRAINT FK_RUTAS_ZONAS FOREIGN KEY (id_zona)
        REFERENCES ZONAS(id_zona)
);
GO

/* =========================================================
   10. PRECIO_BASE
   ========================================================= */
CREATE TABLE PRECIO_BASE (
    id_precio INT NOT NULL,
    precio_base DECIMAL(10,2) NOT NULL,
    CONSTRAINT PK_PRECIO_BASE PRIMARY KEY (id_precio)
);
GO

/* =========================================================
   11. ESTADO_VIAJE
   ========================================================= */
CREATE TABLE ESTADO_VIAJE (
    id_estado INT NOT NULL,
    estado VARCHAR(10) NOT NULL,
    CONSTRAINT PK_ESTADO_VIAJE PRIMARY KEY (id_estado),
    CONSTRAINT UQ_ESTADO_VIAJE_ESTADO UNIQUE (estado)
);
GO

/* =========================================================
   12. NUMERO_UNIDAD
   ========================================================= */
CREATE TABLE NUMERO_UNIDAD (
    id_num_unidad INT NOT NULL,
    unidad VARCHAR(10) NOT NULL,
    CONSTRAINT PK_NUMERO_UNIDAD PRIMARY KEY (id_num_unidad),
    CONSTRAINT UQ_NUMERO_UNIDAD_UNIDAD UNIQUE (unidad)
);
GO

/* =========================================================
   13. MARCA_UNIDAD
   ========================================================= */
CREATE TABLE MARCA_UNIDAD (
    id_marca INT NOT NULL,
    marca VARCHAR(30) NOT NULL,
    CONSTRAINT PK_MARCA_UNIDAD PRIMARY KEY (id_marca),
    CONSTRAINT UQ_MARCA_UNIDAD_MARCA UNIQUE (marca)
);
GO

/* =========================================================
   14. MODELO_UNIDAD
   ========================================================= */
CREATE TABLE MODELO_UNIDAD (
    id_modelo INT NOT NULL,
    modelo VARCHAR(10) NOT NULL,
    CONSTRAINT PK_MODELO_UNIDAD PRIMARY KEY (id_modelo),
    CONSTRAINT UQ_MODELO_UNIDAD_MODELO UNIQUE (modelo)
);
GO

/* =========================================================
   15. ESTADO_UNIDAD
   ========================================================= */
CREATE TABLE ESTADO_UNIDAD (
    id_estado INT NOT NULL,
    estado VARCHAR(20) NOT NULL,
    CONSTRAINT PK_ESTADO_UNIDAD PRIMARY KEY (id_estado),
    CONSTRAINT UQ_ESTADO_UNIDAD_ESTADO UNIQUE (estado)
);
GO

/* =========================================================
   16. TIPOS_AUTOBUS
   ========================================================= */
CREATE TABLE TIPOS_AUTOBUS (
    id_tipo_autobus INT NOT NULL,
    nombre_tipo VARCHAR(30) NOT NULL,
    capacidad_pasajeros INT NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    CONSTRAINT PK_TIPOS_AUTOBUS PRIMARY KEY (id_tipo_autobus),
    CONSTRAINT UQ_TIPOS_AUTOBUS_NOMBRE_TIPO UNIQUE (nombre_tipo)
);
GO

/* =========================================================
   17. AUTOBUSES
   ========================================================= */
CREATE TABLE AUTOBUSES (
    id_autobus INT NOT NULL,
    placa VARCHAR(15) NOT NULL,
    id_num_unidad INT NOT NULL,
    id_marca INT NOT NULL,
    id_modelo INT NOT NULL,
    anio INT NOT NULL,
    capacidad INT NOT NULL,
    id_estado INT NOT NULL,
    id_tipo_autobus INT NOT NULL,
    CONSTRAINT PK_AUTOBUSES PRIMARY KEY (id_autobus),
    CONSTRAINT UQ_AUTOBUSES_PLACA UNIQUE (placa),
    CONSTRAINT FK_AUTOBUSES_NUMERO_UNIDAD FOREIGN KEY (id_num_unidad)
        REFERENCES NUMERO_UNIDAD(id_num_unidad),
    CONSTRAINT FK_AUTOBUSES_MARCA_UNIDAD FOREIGN KEY (id_marca)
        REFERENCES MARCA_UNIDAD(id_marca),
    CONSTRAINT FK_AUTOBUSES_MODELO_UNIDAD FOREIGN KEY (id_modelo)
        REFERENCES MODELO_UNIDAD(id_modelo),
    CONSTRAINT FK_AUTOBUSES_ESTADO_UNIDAD FOREIGN KEY (id_estado)
        REFERENCES ESTADO_UNIDAD(id_estado),
    CONSTRAINT FK_AUTOBUSES_TIPOS_AUTOBUS FOREIGN KEY (id_tipo_autobus)
        REFERENCES TIPOS_AUTOBUS(id_tipo_autobus)
);
GO

/* =========================================================
   18. ESTADO_DEKRA
   ========================================================= */
CREATE TABLE ESTADO_DEKRA (
    id_estado INT NOT NULL,
    estado VARCHAR(10) NOT NULL,
    CONSTRAINT PK_ESTADO_DEKRA PRIMARY KEY (id_estado),
    CONSTRAINT UQ_ESTADO_DEKRA_ESTADO UNIQUE (estado)
);
GO

/* =========================================================
   19. DEKRAS
   ========================================================= */
CREATE TABLE DEKRAS (
    id_dekra INT NOT NULL,
    id_autobus INT NOT NULL,
    numero_dekra VARCHAR(20) NOT NULL,
    fecha_emision DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    id_estado INT NOT NULL,
    CONSTRAINT PK_DEKRAS PRIMARY KEY (id_dekra),
    CONSTRAINT UQ_DEKRAS_NUMERO_DEKRA UNIQUE (numero_dekra),
    CONSTRAINT FK_DEKRAS_AUTOBUSES FOREIGN KEY (id_autobus)
        REFERENCES AUTOBUSES(id_autobus),
    CONSTRAINT FK_DEKRAS_ESTADO_DEKRA FOREIGN KEY (id_estado)
        REFERENCES ESTADO_DEKRA(id_estado)
);
GO

/* =========================================================
   20. ESTADO_MARCHAMO
   ========================================================= */
CREATE TABLE ESTADO_MARCHAMO (
    id_estado INT NOT NULL,
    estado VARCHAR(10) NOT NULL,
    CONSTRAINT PK_ESTADO_MARCHAMO PRIMARY KEY (id_estado),
    CONSTRAINT UQ_ESTADO_MARCHAMO_ESTADO UNIQUE (estado)
);
GO

/* =========================================================
   21. MARCHAMOS
   ========================================================= */
CREATE TABLE MARCHAMOS (
    id_marchamo INT NOT NULL,
    id_autobus INT NOT NULL,
    numero_marchamo VARCHAR(20) NOT NULL,
    periodo VARCHAR(10) NOT NULL,
    fecha_pago DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    id_estado INT NOT NULL,
    CONSTRAINT PK_MARCHAMOS PRIMARY KEY (id_marchamo),
    CONSTRAINT UQ_MARCHAMOS_NUMERO_MARCHAMO UNIQUE (numero_marchamo),
    CONSTRAINT FK_MARCHAMOS_AUTOBUSES FOREIGN KEY (id_autobus)
        REFERENCES AUTOBUSES(id_autobus),
    CONSTRAINT FK_MARCHAMOS_ESTADO_MARCHAMO FOREIGN KEY (id_estado)
        REFERENCES ESTADO_MARCHAMO(id_estado)
);
GO

/* =========================================================
   22. MANTENIMIENTOS_AUTOBUS
   ========================================================= */
CREATE TABLE MANTENIMIENTOS_AUTOBUS (
    id_mantenimiento INT NOT NULL,
    id_autobus INT NOT NULL,
    tipo_mantenimiento VARCHAR(40) NOT NULL,
    descripcion VARCHAR(150) NOT NULL,
    fecha_mantenimiento DATE NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    taller VARCHAR(60) NOT NULL,
    CONSTRAINT PK_MANTENIMIENTOS_AUTOBUS PRIMARY KEY (id_mantenimiento),
    CONSTRAINT FK_MANTENIMIENTOS_AUTOBUS_AUTOBUSES FOREIGN KEY (id_autobus)
        REFERENCES AUTOBUSES(id_autobus)
);
GO

/* =========================================================
   23. VIAJES
   ========================================================= */
CREATE TABLE VIAJES (
    id_viaje INT NOT NULL,
    id_ruta INT NOT NULL,
    id_autobus INT NOT NULL,
    fecha_salida DATE NOT NULL,
    hora_salida TIME NOT NULL,
    id_precio INT NOT NULL,
    cupo_total INT NOT NULL,
    id_estado INT NOT NULL,
    CONSTRAINT PK_VIAJES PRIMARY KEY (id_viaje),
    CONSTRAINT FK_VIAJES_RUTAS FOREIGN KEY (id_ruta)
        REFERENCES RUTAS(id_ruta),
    CONSTRAINT FK_VIAJES_AUTOBUSES FOREIGN KEY (id_autobus)
        REFERENCES AUTOBUSES(id_autobus),
    CONSTRAINT FK_VIAJES_PRECIO_BASE FOREIGN KEY (id_precio)
        REFERENCES PRECIO_BASE(id_precio),
    CONSTRAINT FK_VIAJES_ESTADO_VIAJE FOREIGN KEY (id_estado)
        REFERENCES ESTADO_VIAJE(id_estado)
);
GO

/* =========================================================
   24. VIAJE_PERSONAL
   ========================================================= */
CREATE TABLE VIAJE_PERSONAL (
    id_viaje_personal INT NOT NULL,
    id_viaje INT NOT NULL,
    id_empleado INT NOT NULL,
    funcion_en_viaje VARCHAR(20) NOT NULL,
    CONSTRAINT PK_VIAJE_PERSONAL PRIMARY KEY (id_viaje_personal),
    CONSTRAINT FK_VIAJE_PERSONAL_VIAJES FOREIGN KEY (id_viaje)
        REFERENCES VIAJES(id_viaje),
    CONSTRAINT FK_VIAJE_PERSONAL_EMPLEADOS FOREIGN KEY (id_empleado)
        REFERENCES EMPLEADOS(id_empleado)
);
GO

/* =========================================================
   25. ESTADO_RESERVACION
   ========================================================= */
CREATE TABLE ESTADO_RESERVACION (
    id_estado INT NOT NULL,
    estado VARCHAR(10) NOT NULL,
    CONSTRAINT PK_ESTADO_RESERVACION PRIMARY KEY (id_estado),
    CONSTRAINT UQ_ESTADO_RESERVACION_ESTADO UNIQUE (estado)
);
GO

/* =========================================================
   26. RESERVACIONES
   ========================================================= */
CREATE TABLE RESERVACIONES (
    id_reservacion INT NOT NULL,
    id_cliente INT NOT NULL,
    id_viaje INT NOT NULL,
    id_administrativo INT NOT NULL,
    fecha_reservacion DATE NOT NULL,
    cantidad_pasajeros INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    impuestos DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    id_estado INT NOT NULL,
    CONSTRAINT PK_RESERVACIONES PRIMARY KEY (id_reservacion),
    CONSTRAINT FK_RESERVACIONES_CLIENTES FOREIGN KEY (id_cliente)
        REFERENCES CLIENTES(id_cliente),
    CONSTRAINT FK_RESERVACIONES_VIAJES FOREIGN KEY (id_viaje)
        REFERENCES VIAJES(id_viaje),
    CONSTRAINT FK_RESERVACIONES_EMPLEADOS FOREIGN KEY (id_administrativo)
        REFERENCES EMPLEADOS(id_empleado),
    CONSTRAINT FK_RESERVACIONES_ESTADO_RESERVACION FOREIGN KEY (id_estado)
        REFERENCES ESTADO_RESERVACION(id_estado)
);
GO

/* =========================================================
   27. DETALLE_RESERVACION
   ========================================================= */
CREATE TABLE DETALLE_RESERVACION (
    id_detalle_reservacion INT NOT NULL,
    id_reservacion INT NOT NULL,
    nombre_pasajero VARCHAR(25) NOT NULL,
    apellido_pasajero VARCHAR(25) NOT NULL,
    identificacion_pasajero VARCHAR(20) NOT NULL,
    asiento VARCHAR(10) NOT NULL,
    observaciones VARCHAR(150) NULL,
    CONSTRAINT PK_DETALLE_RESERVACION PRIMARY KEY (id_detalle_reservacion),
    CONSTRAINT FK_DETALLE_RESERVACION_RESERVACIONES FOREIGN KEY (id_reservacion)
        REFERENCES RESERVACIONES(id_reservacion)
);
GO

/* =========================================================
   28. DESCUENTOS
   ========================================================= */
CREATE TABLE DESCUENTOS (
    id_descuento INT NOT NULL,
    tipo_descuento VARCHAR(20) NOT NULL,
    CONSTRAINT PK_DESCUENTOS PRIMARY KEY (id_descuento),
    CONSTRAINT UQ_DESCUENTOS_TIPO_DESCUENTO UNIQUE (tipo_descuento)
);
GO

/* =========================================================
   29. ESTADO_FACTURA
   ========================================================= */
CREATE TABLE ESTADO_FACTURA (
    id_estado INT NOT NULL,
    estado VARCHAR(10) NOT NULL,
    CONSTRAINT PK_ESTADO_FACTURA PRIMARY KEY (id_estado),
    CONSTRAINT UQ_ESTADO_FACTURA_ESTADO UNIQUE (estado)
);
GO

/* =========================================================
   30. FACTURAS
   ========================================================= */
CREATE TABLE FACTURAS (
    id_factura INT NOT NULL,
    id_reservacion INT NOT NULL,
    numero_factura VARCHAR(20) NOT NULL,
    fecha_factura DATE NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    impuesto DECIMAL(10,2) NOT NULL,
    id_descuento INT NULL,
    total DECIMAL(10,2) NOT NULL,
    id_estado INT NOT NULL,
    CONSTRAINT PK_FACTURAS PRIMARY KEY (id_factura),
    CONSTRAINT UQ_FACTURAS_ID_RESERVACION UNIQUE (id_reservacion),
    CONSTRAINT UQ_FACTURAS_NUMERO_FACTURA UNIQUE (numero_factura),
    CONSTRAINT FK_FACTURAS_RESERVACIONES FOREIGN KEY (id_reservacion)
        REFERENCES RESERVACIONES(id_reservacion),
    CONSTRAINT FK_FACTURAS_DESCUENTOS FOREIGN KEY (id_descuento)
        REFERENCES DESCUENTOS(id_descuento),
    CONSTRAINT FK_FACTURAS_ESTADO_FACTURA FOREIGN KEY (id_estado)
        REFERENCES ESTADO_FACTURA(id_estado)
);
GO

/* =========================================================
   31. METODOS_PAGO
   ========================================================= */
CREATE TABLE METODOS_PAGO (
    id_metodo_pago INT NOT NULL,
    nombre_metodo VARCHAR(30) NOT NULL,
    CONSTRAINT PK_METODOS_PAGO PRIMARY KEY (id_metodo_pago),
    CONSTRAINT UQ_METODOS_PAGO_NOMBRE_METODO UNIQUE (nombre_metodo)
);
GO

/* =========================================================
   32. ESTADO_PAGO
   ========================================================= */
CREATE TABLE ESTADO_PAGO (
    id_estado INT NOT NULL,
    estado VARCHAR(10) NOT NULL,
    CONSTRAINT PK_ESTADO_PAGO PRIMARY KEY (id_estado),
    CONSTRAINT UQ_ESTADO_PAGO_ESTADO UNIQUE (estado)
);
GO

/* =========================================================
   33. PAGOS
   ========================================================= */
CREATE TABLE PAGOS (
    id_pago INT NOT NULL,
    id_factura INT NOT NULL,
    id_metodo_pago INT NOT NULL,
    fecha_pago DATE NOT NULL,
    monto_pagado DECIMAL(10,2) NOT NULL,
    referencia_pago VARCHAR(40) NOT NULL,
    id_estado INT NOT NULL,
    CONSTRAINT PK_PAGOS PRIMARY KEY (id_pago),
    CONSTRAINT FK_PAGOS_FACTURAS FOREIGN KEY (id_factura)
        REFERENCES FACTURAS(id_factura),
    CONSTRAINT FK_PAGOS_METODOS_PAGO FOREIGN KEY (id_metodo_pago)
        REFERENCES METODOS_PAGO(id_metodo_pago),
    CONSTRAINT FK_PAGOS_ESTADO_PAGO FOREIGN KEY (id_estado)
        REFERENCES ESTADO_PAGO(id_estado)
);
GO

/* =========================================================
   34. BITACORA
   ========================================================= */
CREATE TABLE BITACORA (
    id_bitacora INT NOT NULL,
    id_empleado INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    accion VARCHAR(50) NOT NULL,
    tabla_afectada VARCHAR(50) NOT NULL,
    id_registro_afectado INT NOT NULL,
    descripcion_evento VARCHAR(200) NOT NULL,
    CONSTRAINT PK_BITACORA PRIMARY KEY (id_bitacora),
    CONSTRAINT FK_BITACORA_EMPLEADOS FOREIGN KEY (id_empleado)
        REFERENCES EMPLEADOS(id_empleado)
);
GO