from core.db_manager import DBManager


class ViajeRepository:
    """
    Acceso a datos del módulo de viajes.
    Toda consulta SQL relacionada con VIAJES vive aquí.
    """

    def __init__(self) -> None:
        self.db = DBManager()

    def listar_viajes(self):
        query = """
        SELECT
            v.id_viaje,
            r.nombre_ruta,
            a.placa,
            v.fecha_salida,
            v.hora_salida,
            pb.precio_base,
            v.cupo_total,
            ev.estado
        FROM VIAJES v
        INNER JOIN RUTAS r
            ON v.id_ruta = r.id_ruta
        INNER JOIN AUTOBUSES a
            ON v.id_autobus = a.id_autobus
        INNER JOIN PRECIO_BASE pb
            ON v.id_precio = pb.id_precio
        INNER JOIN ESTADO_VIAJE ev
            ON v.id_estado = ev.id_estado
        ORDER BY v.id_viaje;
        """
        return self.db.execute(query, fetch=True)

    def obtener_viaje_por_id(self, id_viaje: int):
        query = """
        SELECT
            id_viaje,
            id_ruta,
            id_autobus,
            fecha_salida,
            hora_salida,
            id_precio,
            cupo_total,
            id_estado
        FROM VIAJES
        WHERE id_viaje = ?;
        """
        return self.db.execute(query, (id_viaje,), fetch_one=True)

    def obtener_siguiente_id(self) -> int:
        query = """
        SELECT ISNULL(MAX(id_viaje), 0) + 1
        FROM VIAJES;
        """
        result = self.db.execute(query, fetch_one=True)
        return int(result[0]) if result else 1

    def insertar_viaje(
        self,
        id_viaje: int,
        id_ruta: int,
        id_autobus: int,
        fecha_salida: str,
        hora_salida: str,
        id_precio: int,
        cupo_total: int,
        id_estado: int,
    ) -> None:
        query = """
        INSERT INTO VIAJES (
            id_viaje,
            id_ruta,
            id_autobus,
            fecha_salida,
            hora_salida,
            id_precio,
            cupo_total,
            id_estado
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            id_viaje,
            id_ruta,
            id_autobus,
            fecha_salida,
            hora_salida,
            id_precio,
            cupo_total,
            id_estado,
        )
        self.db.execute(query, params)

    def actualizar_viaje(
        self,
        id_viaje: int,
        id_ruta: int,
        id_autobus: int,
        fecha_salida: str,
        hora_salida: str,
        id_precio: int,
        cupo_total: int,
        id_estado: int,
    ) -> None:
        query = """
        UPDATE VIAJES
        SET
            id_ruta = ?,
            id_autobus = ?,
            fecha_salida = ?,
            hora_salida = ?,
            id_precio = ?,
            cupo_total = ?,
            id_estado = ?
        WHERE id_viaje = ?;
        """
        params = (
            id_ruta,
            id_autobus,
            fecha_salida,
            hora_salida,
            id_precio,
            cupo_total,
            id_estado,
            id_viaje,
        )
        self.db.execute(query, params)

    def eliminar_viaje(self, id_viaje: int) -> None:
        query = """
        DELETE FROM VIAJES
        WHERE id_viaje = ?;
        """
        self.db.execute(query, (id_viaje,))

    def listar_rutas(self):
        query = """
        SELECT id_ruta, nombre_ruta
        FROM RUTAS
        ORDER BY nombre_ruta;
        """
        return self.db.execute(query, fetch=True)

    def listar_autobuses(self):
        query = """
        SELECT id_autobus, placa
        FROM AUTOBUSES
        ORDER BY placa;
        """
        return self.db.execute(query, fetch=True)

    def listar_precios_base(self):
        query = """
        SELECT id_precio, precio_base
        FROM PRECIO_BASE
        ORDER BY id_precio;
        """
        return self.db.execute(query, fetch=True)

    def listar_estados_viaje(self):
        query = """
        SELECT id_estado, estado
        FROM ESTADO_VIAJE
        ORDER BY estado;
        """
        return self.db.execute(query, fetch=True)