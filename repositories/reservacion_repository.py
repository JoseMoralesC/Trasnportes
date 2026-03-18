from core.db_manager import DBManager


class ReservacionRepository:
    """
    Acceso a datos del módulo de reservaciones.
    Toda consulta SQL relacionada con RESERVACIONES vive aquí.
    """

    def __init__(self) -> None:
        self.db = DBManager()

    def listar_reservaciones(self):
        query = """
        SELECT
            r.id_reservacion,
            c.cedula,
            c.nombre,
            c.apellido1,
            c.apellido2,
            v.id_viaje,
            rt.nombre_ruta,
            v.fecha_salida,
            v.hora_salida,
            e.nombre AS nombre_admin,
            e.apellido1 AS apellido_admin,
            r.fecha_reservacion,
            r.cantidad_pasajeros,
            r.subtotal,
            r.impuestos,
            r.total,
            er.estado
        FROM RESERVACIONES r
        INNER JOIN CLIENTES c
            ON r.id_cliente = c.id_cliente
        INNER JOIN VIAJES v
            ON r.id_viaje = v.id_viaje
        INNER JOIN RUTAS rt
            ON v.id_ruta = rt.id_ruta
        INNER JOIN EMPLEADOS e
            ON r.id_administrativo = e.id_empleado
        INNER JOIN ESTADO_RESERVACION er
            ON r.id_estado = er.id_estado
        ORDER BY r.id_reservacion;
        """
        return self.db.execute(query, fetch=True)

    def obtener_reservacion_por_id(self, id_reservacion: int):
        query = """
        SELECT
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
        FROM RESERVACIONES
        WHERE id_reservacion = ?;
        """
        return self.db.execute(query, (id_reservacion,), fetch_one=True)

    def obtener_siguiente_id(self) -> int:
        query = """
        SELECT ISNULL(MAX(id_reservacion), 0) + 1
        FROM RESERVACIONES;
        """
        result = self.db.execute(query, fetch_one=True)
        return int(result[0]) if result else 1

    def insertar_reservacion(
        self,
        id_reservacion: int,
        id_cliente: int,
        id_viaje: int,
        id_administrativo: int,
        fecha_reservacion: str,
        cantidad_pasajeros: int,
        subtotal: float,
        impuestos: float,
        total: float,
        id_estado: int,
    ) -> None:
        query = """
        INSERT INTO RESERVACIONES (
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            id_reservacion,
            id_cliente,
            id_viaje,
            id_administrativo,
            fecha_reservacion,
            cantidad_pasajeros,
            subtotal,
            impuestos,
            total,
            id_estado,
        )
        self.db.execute(query, params)

    def actualizar_reservacion(
        self,
        id_reservacion: int,
        id_cliente: int,
        id_viaje: int,
        id_administrativo: int,
        fecha_reservacion: str,
        cantidad_pasajeros: int,
        subtotal: float,
        impuestos: float,
        total: float,
        id_estado: int,
    ) -> None:
        query = """
        UPDATE RESERVACIONES
        SET
            id_cliente = ?,
            id_viaje = ?,
            id_administrativo = ?,
            fecha_reservacion = ?,
            cantidad_pasajeros = ?,
            subtotal = ?,
            impuestos = ?,
            total = ?,
            id_estado = ?
        WHERE id_reservacion = ?;
        """
        params = (
            id_cliente,
            id_viaje,
            id_administrativo,
            fecha_reservacion,
            cantidad_pasajeros,
            subtotal,
            impuestos,
            total,
            id_estado,
            id_reservacion,
        )
        self.db.execute(query, params)

    def eliminar_reservacion(self, id_reservacion: int) -> None:
        query = """
        DELETE FROM RESERVACIONES
        WHERE id_reservacion = ?;
        """
        self.db.execute(query, (id_reservacion,))

    def listar_clientes(self):
        query = """
        SELECT
            id_cliente,
            cedula,
            nombre,
            apellido1,
            apellido2
        FROM CLIENTES
        ORDER BY nombre, apellido1, apellido2;
        """
        return self.db.execute(query, fetch=True)

    def listar_viajes(self):
        query = """
        SELECT
            v.id_viaje,
            rt.nombre_ruta,
            v.fecha_salida,
            v.hora_salida
        FROM VIAJES v
        INNER JOIN RUTAS rt
            ON v.id_ruta = rt.id_ruta
        ORDER BY v.id_viaje;
        """
        return self.db.execute(query, fetch=True)

    def listar_empleados_administrativos(self):
        query = """
        SELECT
            e.id_empleado,
            e.nombre,
            e.apellido1,
            re.nombre_rol
        FROM EMPLEADOS e
        INNER JOIN ROLES_EMPLEADO re
            ON e.id_rol = re.id_rol
        ORDER BY e.nombre, e.apellido1;
        """
        return self.db.execute(query, fetch=True)

    def listar_estados_reservacion(self):
        query = """
        SELECT
            id_estado,
            estado
        FROM ESTADO_RESERVACION
        ORDER BY estado;
        """
        return self.db.execute(query, fetch=True)

    def obtener_precio_base_viaje(self, id_viaje: int):
        query = """
        SELECT
            pb.precio_base
        FROM VIAJES v
        INNER JOIN PRECIO_BASE pb
            ON v.id_precio = pb.id_precio
        WHERE v.id_viaje = ?;
        """
        return self.db.execute(query, (id_viaje,), fetch_one=True)
    
    def obtener_pasajeros_reservados(self, id_viaje: int):
        query = """
        SELECT ISNULL(SUM(cantidad_pasajeros), 0)
        FROM RESERVACIONES
        WHERE id_viaje = ?;
        """
        result = self.db.execute(query, (id_viaje,), fetch_one=True)
        return int(result[0]) if result else 0