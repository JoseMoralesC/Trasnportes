USE Proyecto1_Transportes_SA;
GO

/* Datos de prueba - 15 tuplas minimo por tabla */

/* 1. PROFESIONES */
INSERT INTO PROFESIONES (id_profesion, nombre_profesion) VALUES
(1, 'Docente'),
(2, 'Ingeniero'),
(3, 'Contador'),
(4, 'Abogado'),
(5, 'Medico'),
(6, 'Enfermero'),
(7, 'Arquitecto'),
(8, 'Administ'),
(9, 'Disenador'),
(10, 'Programad'),
(11, 'Tecnico'),
(12, 'Mercadeo'),
(13, 'Psicologo'),
(14, 'Electric'),
(15, 'Chef');
GO

/* 2. EMPRESAS */
INSERT INTO EMPRESAS (id_empresa, nombre_empresa, telefono, direccion) VALUES
(1, 'Universidad de Cartago', '2530-1842', 'Cartago Centro, Cartago'),
(2, 'TecnoRed CR S.A.', '2291-3478', 'La Uruca, San Jose'),
(3, 'Agroindustrial Turrialba', '2556-4821', 'Turrialba, Cartago'),
(4, 'Hospital Metropolitano', '2521-6634', 'San Jose, San Jose'),
(5, 'Constructora Valle Central', '2283-1956', 'Curridabat, San Jose'),
(6, 'Hotel Brisas del Irazu', '2591-4407', 'Tierra Blanca, Cartago'),
(7, 'Distribuidora Los Angeles', '2257-3984', 'Heredia Centro, Heredia'),
(8, 'Servicios Logisticos del Este', '2236-5712', 'Tres Rios, Cartago'),
(9, 'Finanzas Integrales CR', '2248-6105', 'San Pedro, San Jose'),
(10, 'Turismo Pacuare', '2558-2349', 'Siquirres, Limon'),
(11, 'Cooperativa La Union', '2278-1446', 'La Union, Cartago'),
(12, 'Farmacia Central CR', '2234-7695', 'Alajuela Centro, Alajuela'),
(13, 'Grupo Comercial Orosi', '2533-6071', 'Orosi, Cartago'),
(14, 'Manufactura El Guarco', '2574-2218', 'El Guarco, Cartago'),
(15, 'Consultores Delta CR', '2289-5310', 'Escazu, San Jose');
GO

/* 3. RANGOS_SALARIALES */
INSERT INTO RANGOS_SALARIALES (id_rango_salarial, descripcion_rango, salario_min, salario_max) VALUES
(1, 'Muy bajo', 350000, 449999.99),
(2, 'Bajo', 450000, 549999.99),
(3, 'Medio bajo', 550000, 649999.99),
(4, 'Medio', 650000, 799999.99),
(5, 'Medio alto', 800000, 949999.99),
(6, 'Alto', 950000, 1199999.99),
(7, 'Muy alto', 1200000, 1499999.99),
(8, 'Ejecutivo I', 1500000, 1799999.99),
(9, 'Ejecutivo II', 1800000, 2199999.99),
(10, 'Gerencial I', 2200000, 2599999.99),
(11, 'Gerencial II', 2600000, 2999999.99),
(12, 'Especial I', 3000000, 3399999.99),
(13, 'Especial II', 3400000, 3799999.99),
(14, 'Direccion', 3800000, 4499999.99),
(15, 'Alta dir', 4500000, 6000000);
GO

/* 4. ROLES_EMPLEADO */
INSERT INTO ROLES_EMPLEADO (id_rol, nombre_rol) VALUES
(1, 'Admin'),
(2, 'Chofer'),
(3, 'Asistente'),
(4, 'Supervisor'),
(5, 'Fiscal'),
(6, 'Cajero'),
(7, 'Jefe Ope'),
(8, 'Mecanico'),
(9, 'Contador'),
(10, 'Analista'),
(11, 'Coordina'),
(12, 'Despacho'),
(13, 'Inspector'),
(14, 'CallCtr'),
(15, 'Gerente');
GO

/* 5. LICENCIAS_CONDUCIR */
INSERT INTO LICENCIAS_CONDUCIR (id_licencia, tipo_licencia, descripcion) VALUES
(1, 'A1', 'Motocicleta'),
(2, 'B1', 'Liviano'),
(3, 'B2', 'Liviano plus'),
(4, 'B3', 'Microbus'),
(5, 'C1', 'Carga ligera'),
(6, 'C2', 'Autobus'),
(7, 'C3', 'Pesado'),
(8, 'D1', 'Taxi'),
(9, 'D2', 'Buseta'),
(10, 'E1', 'Remolque'),
(11, 'E2', 'Rem pesado'),
(12, 'A2', 'Moto grande'),
(13, 'C4', 'Equipo esp'),
(14, 'B4', 'Micro ampli'),
(15, 'D3', 'Trans esp');
GO

/* 6. ZONAS */
INSERT INTO ZONAS (id_zona, nombre_zona) VALUES
(1, 'Cartago'),
(2, 'San Jose'),
(3, 'Heredia'),
(4, 'Alajuela'),
(5, 'Limon'),
(6, 'Puntarenas'),
(7, 'Guanacaste'),
(8, 'Los Santos'),
(9, 'Zona Norte'),
(10, 'Atlantico'),
(11, 'Valle Ctral'),
(12, 'Pac Central'),
(13, 'Pac Sur'),
(14, 'Caribe Sur'),
(15, 'Occidente');
GO

/* 7. PRECIO_BASE */
INSERT INTO PRECIO_BASE (id_precio, precio_base) VALUES
(1, 3500),
(2, 4200),
(3, 4800),
(4, 5500),
(5, 6200),
(6, 7000),
(7, 7800),
(8, 8600),
(9, 9400),
(10, 10300),
(11, 11200),
(12, 12100),
(13, 13000),
(14, 14250),
(15, 15500);
GO

/* 8. ESTADO_VIAJE */
INSERT INTO ESTADO_VIAJE (id_estado, estado) VALUES
(1, 'Prog'),
(2, 'Abord'),
(3, 'Ruta'),
(4, 'Comp'),
(5, 'Cancel'),
(6, 'Reprog'),
(7, 'Lleno'),
(8, 'Delay'),
(9, 'Suspen'),
(10, 'Espera'),
(11, 'Public'),
(12, 'Cierre'),
(13, 'Abierto'),
(14, 'Conf'),
(15, 'Final');
GO

/* 9. NUMERO_UNIDAD */
INSERT INTO NUMERO_UNIDAD (id_num_unidad, unidad) VALUES
(1, 'U-001'),
(2, 'U-002'),
(3, 'U-003'),
(4, 'U-004'),
(5, 'U-005'),
(6, 'U-006'),
(7, 'U-007'),
(8, 'U-008'),
(9, 'U-009'),
(10, 'U-010'),
(11, 'U-011'),
(12, 'U-012'),
(13, 'U-013'),
(14, 'U-014'),
(15, 'U-015');
GO

/* 10. MARCA_UNIDAD */
INSERT INTO MARCA_UNIDAD (id_marca, marca) VALUES
(1, 'Mercedes'),
(2, 'Hino'),
(3, 'Volvo'),
(4, 'Scania'),
(5, 'Yutong'),
(6, 'BlueBird'),
(7, 'Isuzu'),
(8, 'MAN'),
(9, 'Marcopolo'),
(10, 'Hyundai'),
(11, 'Toyota'),
(12, 'JAC'),
(13, 'KingLong'),
(14, 'Mitsu'),
(15, 'Freight');
GO

/* 11. MODELO_UNIDAD */
INSERT INTO MODELO_UNIDAD (id_modelo, modelo) VALUES
(1, 'OF-1721'),
(2, 'H350'),
(3, 'B7R'),
(4, 'K310'),
(5, 'P1200'),
(6, 'C325'),
(7, 'Invictus'),
(8, 'XMQ6127'),
(9, 'Rosa'),
(10, 'N10'),
(11, 'Sideral'),
(12, 'Century'),
(13, 'Torino'),
(14, 'VBuss'),
(15, 'GViale');
GO

/* 12. ESTADO_UNIDAD */
INSERT INTO ESTADO_UNIDAD (id_estado, estado) VALUES
(1, 'Disp'),
(2, 'En ruta'),
(3, 'Mantto'),
(4, 'Reserv'),
(5, 'Fuera'),
(6, 'Limpieza'),
(7, 'Inspec'),
(8, 'Taller'),
(9, 'Asign'),
(10, 'Listo'),
(11, 'Activo'),
(12, 'Inactivo'),
(13, 'Pend'),
(14, 'Patio'),
(15, 'Opera');
GO

/* 13. TIPOS_AUTOBUS */
INSERT INTO TIPOS_AUTOBUS (id_tipo_autobus, nombre_tipo, capacidad_pasajeros, descripcion) VALUES
(1, 'Microbus', 20, 'Ruta corta'),
(2, 'Buseta', 30, 'Traslado urbano'),
(3, 'Ejecutivo', 40, 'Asiento reclinable'),
(4, 'Estandar', 44, 'Servicio regular'),
(5, 'Lujo', 46, 'Servicio premium'),
(6, 'Turistico', 50, 'Giras y tours'),
(7, 'Doble piso', 70, 'Alta capacidad'),
(8, 'Minivan', 12, 'Grupo pequeno'),
(9, 'Coach', 42, 'Viaje empresa'),
(10, 'Interprov', 48, 'Entre provincias'),
(11, 'Urbano', 36, 'GAM'),
(12, 'Escolar', 34, 'Estudiantil'),
(13, 'Aeropuerto', 28, 'Maletero amplio'),
(14, 'Adaptado', 24, 'Accesible'),
(15, 'Semicama', 38, 'Mayor comodidad');
GO

/* 14. ESTADO_DEKRA */
INSERT INTO ESTADO_DEKRA (id_estado, estado) VALUES
(1, 'Vigente'),
(2, 'PrVencer'),
(3, 'Vencido'),
(4, 'Renovado'),
(5, 'Pendiente'),
(6, 'Aprobado'),
(7, 'Observado'),
(8, 'Cancelado'),
(9, 'Suspend'),
(10, 'Tramite'),
(11, 'AlDia'),
(12, 'N/A'),
(13, 'Rechazado'),
(14, 'Emitido'),
(15, 'Validado');
GO

/* 15. ESTADO_MARCHAMO */
INSERT INTO ESTADO_MARCHAMO (id_estado, estado) VALUES
(1, 'Vigente'),
(2, 'PrVencer'),
(3, 'Vencido'),
(4, 'Renovado'),
(5, 'Pendiente'),
(6, 'Aprobado'),
(7, 'Observado'),
(8, 'Cancelado'),
(9, 'Suspend'),
(10, 'Tramite'),
(11, 'AlDia'),
(12, 'N/A'),
(13, 'Rechazado'),
(14, 'Emitido'),
(15, 'Validado');
GO

/* 16. ESTADO_RESERVACION */
INSERT INTO ESTADO_RESERVACION (id_estado, estado) VALUES
(1, 'Activa'),
(2, 'Confirma'),
(3, 'Pendiente'),
(4, 'Cancelada'),
(5, 'Finaliza'),
(6, 'Reprog'),
(7, 'Espera'),
(8, 'Pagada'),
(9, 'Parcial'),
(10, 'Bloqueada'),
(11, 'Vencida'),
(12, 'CheckIn'),
(13, 'Abordada'),
(14, 'NoShow'),
(15, 'Cerrada');
GO

/* 17. DESCUENTOS */
INSERT INTO DESCUENTOS (id_descuento, tipo_descuento) VALUES
(1, 'Sin dto'),
(2, 'Adulto m.'),
(3, 'Estudian.'),
(4, 'Promo web'),
(5, 'Convenio'),
(6, 'Temp baja'),
(7, 'Frecuente'),
(8, 'Tour grp'),
(9, 'Nino'),
(10, 'Funcionario'),
(11, 'Anivers.'),
(12, 'Madrugada'),
(13, 'Promo app'),
(14, 'Regreso'),
(15, 'Social');
GO

/* 18. ESTADO_FACTURA */
INSERT INTO ESTADO_FACTURA (id_estado, estado) VALUES
(1, 'Emitida'),
(2, 'Pagada'),
(3, 'Pendiente'),
(4, 'Anulada'),
(5, 'Vencida'),
(6, 'Parcial'),
(7, 'Proceso'),
(8, 'Credito'),
(9, 'Cobrada'),
(10, 'Revision'),
(11, 'Aprobada'),
(12, 'Rechazo'),
(13, 'Cerrada'),
(14, 'Abierta'),
(15, 'Reserva');
GO

/* 19. METODOS_PAGO */
INSERT INTO METODOS_PAGO (id_metodo_pago, nombre_metodo) VALUES
(1, 'Efectivo'),
(2, 'Debito'),
(3, 'Credito'),
(4, 'SINPE'),
(5, 'Transf'),
(6, 'Deposito'),
(7, 'Pago web'),
(8, 'PayPal'),
(9, 'Link pago'),
(10, 'Datafono'),
(11, 'Cheque'),
(12, 'CredInt'),
(13, 'Puntos'),
(14, 'QR bank'),
(15, 'Mixto');
GO

/* 20. ESTADO_PAGO */
INSERT INTO ESTADO_PAGO (id_estado, estado) VALUES
(1, 'Aplicado'),
(2, 'Pendiente'),
(3, 'Rechazado'),
(4, 'Anulado'),
(5, 'Proceso'),
(6, 'Parcial'),
(7, 'Confirm'),
(8, 'Revision'),
(9, 'Devuelto'),
(10, 'Vencido'),
(11, 'Registro'),
(12, 'Autoriz'),
(13, 'Acredita'),
(14, 'Observa'),
(15, 'Cerrado');
GO

/* 21. CLIENTES */
INSERT INTO CLIENTES (id_cliente, cedula, nombre, apellido1, apellido2, id_profesion, id_empresa, id_rango_salarial, telefono, correo, direccion) VALUES
(1, '1-1001-2001', 'Daniel', 'Rojas', 'Solis', 1, 1, 1, '2276-1822', 'daniel.rojas@correo.cr', 'Cartago Centro, Cartago'),
(2, '1-1002-2002', 'Mariana', 'Vargas', 'Chaves', 2, 2, 2, '2287-1959', 'mariana.vargas@correo.cr', 'Tres Rios, Cartago'),
(3, '1-1003-2003', 'Jose Pablo', 'Mora', 'Calderon', 3, 3, 3, '2298-2096', 'jose.mora@correo.cr', 'Turrialba, Cartago'),
(4, '1-1004-2004', 'Andrea', 'Ramirez', 'Urena', 4, 4, 4, '2410-2233', 'andrea.ramirez@correo.cr', 'Paraiso, Cartago'),
(5, '1-1005-2005', 'Luis Diego', 'Cespedes', 'Mata', 5, 5, 5, '2431-2370', 'luis.cespedes@correo.cr', 'Oreamuno, Cartago'),
(6, '1-1006-2006', 'Valeria', 'Solano', 'Quesada', 6, 6, 6, '2442-2507', 'valeria.solano@correo.cr', 'El Guarco, Cartago'),
(7, '1-1007-2007', 'Kevin', 'Araya', 'Jimenez', 7, 7, 7, '2453-2644', 'kevin.araya@correo.cr', 'Taras, Cartago'),
(8, '1-1008-2008', 'Paola', 'Chacon', 'Rojas', 8, 8, 8, '2464-2781', 'paola.chacon@correo.cr', 'San Rafael, Cartago'),
(9, '3-1009-2009', 'Steven', 'Cordero', 'Navarro', 9, 9, 9, '2475-2918', 'steven.cordero@correo.cr', 'Cervantes, Cartago'),
(10, '3-1010-2010', 'Karla', 'Badilla', 'Vega', 10, 10, 10, '6001-3055', 'karla.badilla@correo.cr', 'Tejar, Cartago'),
(11, '3-1011-2011', 'Bryan', 'Villalobos', 'Salas', 11, 11, 11, '6102-3192', 'bryan.villalobos@correo.cr', 'Pacayas, Cartago'),
(12, '3-1012-2012', 'Natalia', 'Porras', 'Mendez', 12, 12, 12, '6203-3329', 'natalia.porras@correo.cr', 'Juan Vinas, Cartago'),
(13, '3-1013-2013', 'Esteban', 'Abarca', 'Lopez', 13, 13, 13, '6304-3466', 'esteban.abarca@correo.cr', 'Tobosi, Cartago'),
(14, '3-1014-2014', 'Sofia', 'Madrigal', 'Ruiz', 14, 14, 14, '6405-3603', 'sofia.madrigal@correo.cr', 'Orosi, Cartago'),
(15, '3-1015-2015', 'Fabricio', 'Guerrero', 'Alfaro', 15, 15, 15, '6506-3740', 'fabricio.guerrero@correo.cr', 'Cot, Cartago');
GO

/* 22. EMPLEADOS */
INSERT INTO EMPLEADOS (id_empleado, cedula, nombre, apellido1, apellido2, telefono, correo, fecha_ingreso, id_rol, id_licencia) VALUES
(1, '2-1101-2101', 'Melissa', 'Soto', 'Bonilla', '8102-5247', 'melissa.soto@transportescr.com', '2021-02-21', 1, NULL),
(2, '2-1102-2102', 'Gerardo', 'Leiva', 'Castro', '8203-5384', 'gerardo.leiva@transportescr.com', '2021-03-30', 2, 6),
(3, '2-1103-2103', 'Camila', 'Segura', 'Mora', '8304-5521', 'camila.segura@transportescr.com', '2021-05-06', 3, NULL),
(4, '2-1104-2104', 'Javier', 'Brenes', 'Campos', '8405-5658', 'javier.brenes@transportescr.com', '2021-06-12', 4, 7),
(5, '2-1105-2105', 'Noelia', 'Ugalde', 'Hidalgo', '8506-5795', 'noelia.ugalde@transportescr.com', '2021-07-19', 5, 3),
(6, '2-1106-2106', 'Allan', 'Barboza', 'Rojas', '8607-5932', 'allan.barboza@transportescr.com', '2021-08-25', 6, NULL),
(7, '2-1107-2107', 'Daniela', 'Monge', 'Cruz', '8708-6069', 'daniela.monge@transportescr.com', '2021-10-01', 7, NULL),
(8, '2-1108-2108', 'Mauricio', 'Fonseca', 'Sanchez', '8809-6206', 'mauricio.fonseca@transportescr.com', '2021-11-07', 8, 6),
(9, '1-1109-2109', 'Gabriela', 'Salazar', 'Herrera', '8901-6343', 'gabriela.salazar@transportescr.com', '2021-12-14', 9, NULL),
(10, '1-1110-2110', 'Ronald', 'Mena', 'Valverde', '2210-6480', 'ronald.mena@transportescr.com', '2022-01-20', 10, 7),
(11, '1-1111-2111', 'Ana Lucia', 'Zuniga', 'Mora', '2221-6617', 'ana.zuniga@transportescr.com', '2022-02-26', 11, NULL),
(12, '1-1112-2112', 'Carlos Andres', 'Rosales', 'Jimenez', '2232-6754', 'carlos.rosales@transportescr.com', '2022-04-04', 12, 6),
(13, '1-1113-2113', 'Lucia', 'Bolanos', 'Murillo', '2243-6891', 'lucia.bolanos@transportescr.com', '2022-05-11', 13, NULL),
(14, '1-1114-2114', 'Ricardo', 'Aguilar', 'Paniagua', '2254-7028', 'ricardo.aguilar@transportescr.com', '2022-06-17', 14, 6),
(15, '1-1115-2115', 'Priscila', 'Arias', 'Quesada', '2265-7165', 'priscila.arias@transportescr.com', '2022-07-24', 15, 3);
GO

/* 23. RUTAS */
INSERT INTO RUTAS (id_ruta, nombre_ruta, origen, destino, distancia_km, duracion_estimada, id_zona) VALUES
(1, 'Cartago-San Jose', 'Cartago', 'San Jose', 24.50, '01:00', 1),
(2, 'Cartago-Heredia', 'Cartago', 'Heredia', 36.20, '01:20', 2),
(3, 'Cartago-Alajuela', 'Cartago', 'Alajuela', 48.10, '01:40', 3),
(4, 'Cartago-Limon', 'Cartago', 'Limon', 107.40, '02:30', 5),
(5, 'San Jose-Puntarenas', 'San Jose', 'Puntarenas', 95.00, '02:10', 6),
(6, 'San Jose-Liberia', 'San Jose', 'Liberia', 210.30, '04:10', 7),
(7, 'Heredia-Cartago', 'Heredia', 'Cartago', 34.80, '01:15', 11),
(8, 'Turrialba-San Jose', 'Turrialba', 'San Jose', 66.50, '01:45', 10),
(9, 'Paraiso-Cartago', 'Paraiso', 'Cartago', 8.50, '00:20', 1),
(10, 'Tres Rios-San Jose', 'Tres Rios', 'San Jose', 14.20, '00:35', 11),
(11, 'Orosi-Cartago', 'Orosi', 'Cartago', 19.00, '00:40', 1),
(12, 'Cartago-Dota', 'Cartago', 'Dota', 55.50, '01:50', 8),
(13, 'Alajuela-Fortuna', 'Alajuela', 'Fortuna', 135.00, '03:00', 9),
(14, 'Limon-PViejo', 'Limon', 'Pto Viejo', 63.40, '01:30', 14),
(15, 'Quepos-Golfito', 'Quepos', 'Golfito', 162.00, '03:40', 13);
GO

/* 24. AUTOBUSES */
INSERT INTO AUTOBUSES (id_autobus, placa, id_num_unidad, id_marca, id_modelo, anio, capacidad, id_estado, id_tipo_autobus) VALUES
(1, 'BUS-1001', 1, 1, 1, 2016, 40, 1, 1),
(2, 'BUS-1002', 2, 2, 2, 2017, 30, 2, 2),
(3, 'BUS-1003', 3, 3, 3, 2018, 44, 3, 3),
(4, 'BUS-1004', 4, 4, 4, 2019, 46, 4, 4),
(5, 'BUS-1005', 5, 5, 5, 2020, 50, 5, 5),
(6, 'BUS-1006', 6, 6, 6, 2021, 48, 6, 6),
(7, 'BUS-1007', 7, 7, 7, 2015, 36, 7, 7),
(8, 'BUS-1008', 8, 8, 8, 2022, 20, 8, 8),
(9, 'BUS-1009', 9, 9, 9, 2018, 42, 9, 9),
(10, 'BUS-1010', 10, 10, 10, 2017, 38, 10, 10),
(11, 'BUS-1011', 11, 11, 11, 2023, 28, 11, 11),
(12, 'BUS-1012', 12, 12, 12, 2019, 34, 12, 12),
(13, 'BUS-1013', 13, 13, 13, 2016, 24, 13, 13),
(14, 'BUS-1014', 14, 14, 14, 2024, 70, 14, 14),
(15, 'BUS-1015', 15, 15, 15, 2020, 40, 15, 15);
GO

/* 25. DEKRAS */
INSERT INTO DEKRAS (id_dekra, id_autobus, numero_dekra, fecha_emision, fecha_vencimiento, id_estado) VALUES
(1, 1, 'DKR-2025-1001', '2025-01-21', '2026-01-21', 1),
(2, 2, 'DKR-2025-1002', '2025-02-01', '2026-02-01', 2),
(3, 3, 'DKR-2025-1003', '2025-02-12', '2026-02-12', 3),
(4, 4, 'DKR-2025-1004', '2025-02-23', '2026-02-23', 4),
(5, 5, 'DKR-2025-1005', '2025-03-06', '2026-03-06', 5),
(6, 6, 'DKR-2025-1006', '2025-03-17', '2026-03-17', 6),
(7, 7, 'DKR-2025-1007', '2025-03-28', '2026-03-28', 7),
(8, 8, 'DKR-2025-1008', '2025-04-08', '2026-04-08', 8),
(9, 9, 'DKR-2025-1009', '2025-04-19', '2026-04-19', 9),
(10, 10, 'DKR-2025-1010', '2025-04-30', '2026-04-30', 10),
(11, 11, 'DKR-2025-1011', '2025-05-11', '2026-05-11', 11),
(12, 12, 'DKR-2025-1012', '2025-05-22', '2026-05-22', 12),
(13, 13, 'DKR-2025-1013', '2025-06-02', '2026-06-02', 13),
(14, 14, 'DKR-2025-1014', '2025-06-13', '2026-06-13', 14),
(15, 15, 'DKR-2025-1015', '2025-06-24', '2026-06-24', 15);
GO

/* 26. MARCHAMOS */
INSERT INTO MARCHAMOS (id_marchamo, id_autobus, numero_marchamo, periodo, fecha_pago, fecha_vencimiento, id_estado) VALUES
(1, 1, 'MCH-2026-2001', '2026', '2025-12-02', '2026-12-31', 1),
(2, 2, 'MCH-2026-2002', '2026', '2025-12-03', '2026-12-31', 2),
(3, 3, 'MCH-2026-2003', '2026', '2025-12-04', '2026-12-31', 3),
(4, 4, 'MCH-2026-2004', '2026', '2025-12-05', '2026-12-31', 4),
(5, 5, 'MCH-2026-2005', '2026', '2025-12-06', '2026-12-31', 5),
(6, 6, 'MCH-2026-2006', '2026', '2025-12-07', '2026-12-31', 6),
(7, 7, 'MCH-2026-2007', '2026', '2025-12-08', '2026-12-31', 7),
(8, 8, 'MCH-2026-2008', '2026', '2025-12-09', '2026-12-31', 8),
(9, 9, 'MCH-2026-2009', '2026', '2025-12-10', '2026-12-31', 9),
(10, 10, 'MCH-2026-2010', '2026', '2025-12-11', '2026-12-31', 10),
(11, 11, 'MCH-2026-2011', '2026', '2025-12-12', '2026-12-31', 11),
(12, 12, 'MCH-2026-2012', '2026', '2025-12-13', '2026-12-31', 12),
(13, 13, 'MCH-2026-2013', '2026', '2025-12-14', '2026-12-31', 13),
(14, 14, 'MCH-2026-2014', '2026', '2025-12-15', '2026-12-31', 14),
(15, 15, 'MCH-2026-2015', '2026', '2025-12-16', '2026-12-31', 15);
GO

/* 27. MANTENIMIENTOS_AUTOBUS */
INSERT INTO MANTENIMIENTOS_AUTOBUS (id_mantenimiento, id_autobus, tipo_mantenimiento, descripcion, fecha_mantenimiento, costo, taller) VALUES
(1, 1, 'Preventivo', 'Mantenimiento preventivo de unidad 1', '2025-02-10', 102500, 'AutoBus CR'),
(2, 2, 'Correctivo', 'Mantenimiento correctivo de unidad 2', '2025-02-19', 120000, 'Mecanica Este'),
(3, 3, 'Aceite', 'Mantenimiento aceite de unidad 3', '2025-02-28', 137500, 'Servicios Diesel'),
(4, 4, 'Frenos', 'Mantenimiento frenos de unidad 4', '2025-03-09', 155000, 'Taller San Jose'),
(5, 5, 'Llantas', 'Mantenimiento llantas de unidad 5', '2025-03-18', 172500, 'Taller Cartago'),
(6, 6, 'Electrico', 'Mantenimiento electrico de unidad 6', '2025-03-27', 190000, 'AutoBus CR'),
(7, 7, 'Suspension', 'Mantenimiento suspension de unidad 7', '2025-04-05', 207500, 'Mecanica Este'),
(8, 8, 'Alineado', 'Mantenimiento alineado de unidad 8', '2025-04-14', 225000, 'Servicios Diesel'),
(9, 9, 'Tapiceria', 'Mantenimiento tapiceria de unidad 9', '2025-04-23', 242500, 'Taller San Jose'),
(10, 10, 'Pintura', 'Mantenimiento pintura de unidad 10', '2025-05-02', 260000, 'Taller Cartago'),
(11, 11, 'Motor', 'Mantenimiento motor de unidad 11', '2025-05-11', 277500, 'AutoBus CR'),
(12, 12, 'Revision', 'Mantenimiento revision de unidad 12', '2025-05-20', 295000, 'Mecanica Este'),
(13, 13, 'A/C', 'Mantenimiento a/c de unidad 13', '2025-05-29', 312500, 'Servicios Diesel'),
(14, 14, 'ABS', 'Mantenimiento abs de unidad 14', '2025-06-07', 330000, 'Taller San Jose'),
(15, 15, 'Lavado', 'Mantenimiento lavado de unidad 15', '2025-06-16', 347500, 'Taller Cartago');
GO

/* 28. VIAJES */
INSERT INTO VIAJES (id_viaje, id_ruta, id_autobus, fecha_salida, hora_salida, id_precio, cupo_total, id_estado) VALUES
(1, 1, 1, '2026-03-20', '05:30', 1, 40, 1),
(2, 2, 2, '2026-03-21', '06:15', 2, 30, 2),
(3, 3, 3, '2026-03-22', '07:00', 3, 44, 3),
(4, 4, 4, '2026-03-23', '08:30', 4, 46, 4),
(5, 5, 5, '2026-03-24', '09:45', 5, 50, 5),
(6, 6, 6, '2026-03-25', '11:00', 6, 48, 6),
(7, 7, 7, '2026-03-26', '12:30', 7, 36, 7),
(8, 8, 8, '2026-03-27', '13:15', 8, 20, 8),
(9, 9, 9, '2026-03-28', '14:00', 9, 42, 9),
(10, 10, 10, '2026-03-29', '15:30', 10, 38, 10),
(11, 11, 11, '2026-03-30', '16:45', 11, 28, 11),
(12, 12, 12, '2026-03-31', '18:00', 12, 34, 12),
(13, 13, 13, '2026-04-01', '19:15', 13, 24, 13),
(14, 14, 14, '2026-04-02', '20:00', 14, 70, 14),
(15, 15, 15, '2026-04-03', '21:30', 15, 40, 15);
GO

/* 29. VIAJE_PERSONAL */
INSERT INTO VIAJE_PERSONAL (id_viaje_personal, id_viaje, id_empleado, funcion_en_viaje) VALUES
(1, 1, 3, 'Chofer'),
(2, 2, 4, 'Asist'),
(3, 3, 5, 'Fiscal'),
(4, 4, 6, 'Chofer'),
(5, 5, 7, 'Asist'),
(6, 6, 8, 'Superv'),
(7, 7, 9, 'Chofer'),
(8, 8, 10, 'Fiscal'),
(9, 9, 11, 'Chofer'),
(10, 10, 12, 'Asist'),
(11, 11, 13, 'Chofer'),
(12, 12, 14, 'Fiscal'),
(13, 13, 15, 'Chofer'),
(14, 14, 1, 'Asist'),
(15, 15, 2, 'Superv');
GO

/* 30. RESERVACIONES */
INSERT INTO RESERVACIONES (id_reservacion, id_cliente, id_viaje, id_administrativo, fecha_reservacion, cantidad_pasajeros, subtotal, impuestos, total, id_estado) VALUES
(1, 1, 1, 1, '2026-03-02', 1, 3500.00, 455.00, 3955.00, 1),
(2, 2, 2, 1, '2026-03-03', 2, 8400.00, 1092.00, 9492.00, 2),
(3, 3, 3, 6, '2026-03-04', 3, 14400.00, 1872.00, 16272.00, 3),
(4, 4, 4, 1, '2026-03-05', 4, 22000.00, 2860.00, 24860.00, 4),
(5, 5, 5, 1, '2026-03-06', 2, 12400.00, 1612.00, 14012.00, 5),
(6, 6, 6, 6, '2026-03-07', 1, 7000.00, 910.00, 7910.00, 6),
(7, 7, 7, 1, '2026-03-08', 5, 39000.00, 5070.00, 44070.00, 7),
(8, 8, 8, 1, '2026-03-09', 2, 17200.00, 2236.00, 19436.00, 8),
(9, 9, 9, 6, '2026-03-10', 3, 28200.00, 3666.00, 31866.00, 9),
(10, 10, 10, 1, '2026-03-11', 1, 10300.00, 1339.00, 11639.00, 10),
(11, 11, 11, 1, '2026-03-12', 2, 22400.00, 2912.00, 25312.00, 11),
(12, 12, 12, 6, '2026-03-13', 4, 48400.00, 6292.00, 54692.00, 12),
(13, 13, 13, 1, '2026-03-14', 1, 13000.00, 1690.00, 14690.00, 13),
(14, 14, 14, 1, '2026-03-15', 3, 42750.00, 5557.50, 48307.50, 14),
(15, 15, 15, 6, '2026-03-16', 2, 31000.00, 4030.00, 35030.00, 15);
GO

/* 31. DETALLE_RESERVACION */
INSERT INTO DETALLE_RESERVACION (id_detalle_reservacion, id_reservacion, nombre_pasajero, apellido_pasajero, identificacion_pasajero, asiento, observaciones) VALUES
(1, 1, 'Daniel', 'Rojas', '1-1301-2301', 'A1', NULL),
(2, 2, 'Mariana', 'Vargas', '2-1302-2302', 'A2', NULL),
(3, 2, 'Jose Pablo', 'Mora', '1-1303-2303', 'A3', 'Equipaje extra'),
(4, 3, 'Andrea', 'Ramirez', '2-1304-2304', 'A4', NULL),
(5, 3, 'Luis Diego', 'Cespedes', '1-1305-2305', 'B1', NULL),
(6, 3, 'Valeria', 'Solano', '2-1306-2306', 'B2', 'Equipaje extra'),
(7, 4, 'Kevin', 'Araya', '1-1307-2307', 'B3', NULL),
(8, 4, 'Paola', 'Chacon', '2-1308-2308', 'B4', NULL),
(9, 4, 'Steven', 'Cordero', '1-1309-2309', 'C1', 'Equipaje extra'),
(10, 4, 'Karla', 'Badilla', '2-1310-2310', 'C2', NULL),
(11, 5, 'Bryan', 'Villalobos', '1-1311-2311', 'C3', NULL),
(12, 5, 'Natalia', 'Porras', '2-1312-2312', 'C4', 'Equipaje extra'),
(13, 6, 'Esteban', 'Abarca', '1-1313-2313', 'D1', NULL),
(14, 7, 'Sofia', 'Madrigal', '2-1314-2314', 'D2', NULL),
(15, 7, 'Fabricio', 'Guerrero', '1-1315-2315', 'D3', 'Equipaje extra'),
(16, 7, 'Melissa', 'Soto', '2-1316-2316', 'D4', NULL),
(17, 7, 'Gerardo', 'Leiva', '1-1317-2317', 'E1', NULL),
(18, 7, 'Camila', 'Segura', '2-1318-2318', 'E2', 'Equipaje extra'),
(19, 8, 'Javier', 'Brenes', '1-1319-2319', 'E3', NULL),
(20, 8, 'Noelia', 'Ugalde', '2-1320-2320', 'E4', NULL),
(21, 9, 'Allan', 'Barboza', '1-1321-2321', 'A1', 'Equipaje extra'),
(22, 9, 'Daniela', 'Monge', '2-1322-2322', 'A2', NULL),
(23, 9, 'Mauricio', 'Fonseca', '1-1323-2323', 'A3', NULL),
(24, 10, 'Gabriela', 'Salazar', '2-1324-2324', 'A4', 'Equipaje extra'),
(25, 11, 'Ronald', 'Mena', '1-1325-2325', 'B1', NULL),
(26, 11, 'Ana Lucia', 'Zuniga', '2-1326-2326', 'B2', NULL),
(27, 12, 'Carlos Andres', 'Rosales', '1-1327-2327', 'B3', 'Equipaje extra'),
(28, 12, 'Lucia', 'Bolanos', '2-1328-2328', 'B4', NULL),
(29, 12, 'Ricardo', 'Aguilar', '1-1329-2329', 'C1', NULL),
(30, 12, 'Priscila', 'Arias', '2-1330-2330', 'C2', 'Equipaje extra'),
(31, 13, 'Daniel', 'Rojas', '1-1331-2331', 'C3', NULL),
(32, 14, 'Mariana', 'Vargas', '2-1332-2332', 'C4', NULL),
(33, 14, 'Jose Pablo', 'Mora', '1-1333-2333', 'D1', 'Equipaje extra'),
(34, 14, 'Andrea', 'Ramirez', '2-1334-2334', 'D2', NULL),
(35, 15, 'Luis Diego', 'Cespedes', '1-1335-2335', 'D3', NULL),
(36, 15, 'Valeria', 'Solano', '2-1336-2336', 'D4', 'Equipaje extra');
GO

/* 32. FACTURAS */
INSERT INTO FACTURAS (id_factura, id_reservacion, numero_factura, fecha_factura, subtotal, impuesto, id_descuento, total, id_estado) VALUES
(1, 1, 'FAC-2026-0001', '2026-03-03', 3500.00, 455.00, NULL, 3955.00, 1),
(2, 2, 'FAC-2026-0002', '2026-03-04', 8400.00, 1092.00, 2, 8992.00, 2),
(3, 3, 'FAC-2026-0003', '2026-03-05', 14400.00, 1872.00, 3, 15772.00, 3),
(4, 4, 'FAC-2026-0004', '2026-03-06', 22000.00, 2860.00, 4, 24360.00, 4),
(5, 5, 'FAC-2026-0005', '2026-03-07', 12400.00, 1612.00, 5, 13012.00, 5),
(6, 6, 'FAC-2026-0006', '2026-03-08', 7000.00, 910.00, 6, 6910.00, 6),
(7, 7, 'FAC-2026-0007', '2026-03-09', 39000.00, 5070.00, 7, 43070.00, 7),
(8, 8, 'FAC-2026-0008', '2026-03-10', 17200.00, 2236.00, 8, 18436.00, 8),
(9, 9, 'FAC-2026-0009', '2026-03-11', 28200.00, 3666.00, 9, 30866.00, 9),
(10, 10, 'FAC-2026-0010', '2026-03-12', 10300.00, 1339.00, 10, 10639.00, 10),
(11, 11, 'FAC-2026-0011', '2026-03-13', 22400.00, 2912.00, 11, 24312.00, 11),
(12, 12, 'FAC-2026-0012', '2026-03-14', 48400.00, 6292.00, 12, 53692.00, 12),
(13, 13, 'FAC-2026-0013', '2026-03-15', 13000.00, 1690.00, 13, 13690.00, 13),
(14, 14, 'FAC-2026-0014', '2026-03-16', 42750.00, 5557.50, 14, 47307.50, 14),
(15, 15, 'FAC-2026-0015', '2026-03-17', 31000.00, 4030.00, 15, 34030.00, 15);
GO

/* 33. PAGOS */
INSERT INTO PAGOS (id_pago, id_factura, id_metodo_pago, fecha_pago, monto_pagado, referencia_pago, id_estado) VALUES
(1, 1, 1, '2026-03-04', 3955.00, 'EFECTIVO-300001', 1),
(2, 2, 2, '2026-03-05', 8992.00, 'DEBITO-300002', 2),
(3, 3, 3, '2026-03-06', 15772.00, 'CREDITO-300003', 3),
(4, 4, 4, '2026-03-07', 24360.00, 'SINPE-300004', 4),
(5, 5, 5, '2026-03-08', 13012.00, 'TRANSF-300005', 5),
(6, 6, 6, '2026-03-09', 6910.00, 'DEPOSITO-300006', 6),
(7, 7, 7, '2026-03-10', 43070.00, 'PAGOWEB-300007', 7),
(8, 8, 8, '2026-03-11', 18436.00, 'PAYPAL-300008', 8),
(9, 9, 9, '2026-03-12', 30866.00, 'LINKPAGO-300009', 9),
(10, 10, 10, '2026-03-13', 10639.00, 'DATAFONO-300010', 10),
(11, 11, 11, '2026-03-14', 24312.00, 'CHEQUE-300011', 11),
(12, 12, 12, '2026-03-15', 53692.00, 'CREDINT-300012', 12),
(13, 13, 13, '2026-03-16', 13690.00, 'PUNTOS-300013', 13),
(14, 14, 14, '2026-03-17', 47307.50, 'QRBANK-300014', 14),
(15, 15, 15, '2026-03-18', 34030.00, 'MIXTO-300015', 15);
GO

/* 34. BITACORA */
INSERT INTO BITACORA (id_bitacora, id_empleado, fecha_hora, accion, tabla_afectada, id_registro_afectado, descripcion_evento) VALUES
(1, 2, '2026-03-01 13:00:00', 'INSERT', 'CLIENTES', 1, 'Evento insert en CLIENTES registro 1'),
(2, 3, '2026-03-01 18:00:00', 'UPDATE', 'AUTOBUSES', 2, 'Evento update en AUTOBUSES registro 2'),
(3, 4, '2026-03-01 23:00:00', 'LOGIN', 'EMPLEADOS', 3, 'Evento login en EMPLEADOS registro 3'),
(4, 5, '2026-03-02 04:00:00', 'INSERT', 'RUTAS', 4, 'Evento insert en RUTAS registro 4'),
(5, 6, '2026-03-02 09:00:00', 'UPDATE', 'VIAJES', 5, 'Evento update en VIAJES registro 5'),
(6, 7, '2026-03-02 14:00:00', 'DELETE', 'PAGOS', 6, 'Evento delete en PAGOS registro 6'),
(7, 8, '2026-03-02 19:00:00', 'CONSULTA', 'FACTURAS', 7, 'Evento consulta en FACTURAS registro 7'),
(8, 9, '2026-03-03 00:00:00', 'INSERT', 'RESERVACIONES', 8, 'Evento insert en RESERVACIONES registro 8'),
(9, 10, '2026-03-03 05:00:00', 'UPDATE', 'DEKRAS', 9, 'Evento update en DEKRAS registro 9'),
(10, 11, '2026-03-03 10:00:00', 'CONSULTA', 'MARCHAMOS', 10, 'Evento consulta en MARCHAMOS registro 10'),
(11, 12, '2026-03-03 15:00:00', 'PAGO', 'MANTENIMIENTOS_AUTOBUS', 11, 'Evento pago en MANTENIMIENTOS_AUTOBUS registro 11'),
(12, 13, '2026-03-03 20:00:00', 'FACTURA', 'BITACORA', 12, 'Evento factura en BITACORA registro 12'),
(13, 14, '2026-03-04 01:00:00', 'RESERVA', 'RESERVACIONES', 13, 'Evento reserva en RESERVACIONES registro 13'),
(14, 15, '2026-03-04 06:00:00', 'VIAJE', 'AUTOBUSES', 14, 'Evento viaje en AUTOBUSES registro 14'),
(15, 1, '2026-03-04 11:00:00', 'AUDITORIA', 'CLIENTES', 15, 'Evento auditoria en CLIENTES registro 15');
GO
