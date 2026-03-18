from core.db_manager import DBManager


class FacturaRepository:
    """
    Acceso a datos del módulo de facturas.
    Toda consulta SQL relacionada con FACTURAS vive aquí.
    """

    def __init__(self) -> None:
        self.db = DBManager()

    def listar_facturas(self):
        query = """
        SELECT
            f.id_factura,
            f.id_reservacion,
            f.numero_factura,
            f.fecha_factura,
            f.subtotal,
            f.impuesto,
            d.tipo_descuento,
            f.total,
            ef.estado
        FROM FACTURAS f
        INNER JOIN RESERVACIONES r
            ON f.id_reservacion = r.id_reservacion
        LEFT JOIN DESCUENTOS d
            ON f.id_descuento = d.id_descuento
        INNER JOIN ESTADO_FACTURA ef
            ON f.id_estado = ef.id_estado
        ORDER BY f.id_factura;
        """
        return self.db.execute(query, fetch=True)

    def obtener_factura_por_id(self, id_factura: int):
        query = """
        SELECT
            id_factura,
            id_reservacion,
            numero_factura,
            fecha_factura,
            subtotal,
            impuesto,
            id_descuento,
            total,
            id_estado
        FROM FACTURAS
        WHERE id_factura = ?;
        """
        return self.db.execute(query, (id_factura,), fetch_one=True)

    def existe_numero_factura(self, numero_factura: str) -> bool:
        query = """
        SELECT 1
        FROM FACTURAS
        WHERE numero_factura = ?;
        """
        result = self.db.execute(query, (numero_factura,), fetch_one=True)
        return result is not None

    def existe_factura_para_reservacion(self, id_reservacion: int) -> bool:
        query = """
        SELECT 1
        FROM FACTURAS
        WHERE id_reservacion = ?;
        """
        result = self.db.execute(query, (id_reservacion,), fetch_one=True)
        return result is not None

    def obtener_siguiente_id(self) -> int:
        query = """
        SELECT ISNULL(MAX(id_factura), 0) + 1
        FROM FACTURAS;
        """
        result = self.db.execute(query, fetch_one=True)
        return int(result[0]) if result else 1

    def insertar_factura(
        self,
        id_factura: int,
        id_reservacion: int,
        numero_factura: str,
        fecha_factura: str,
        subtotal: float,
        impuesto: float,
        id_descuento: int | None,
        total: float,
        id_estado: int,
    ) -> None:
        query = """
        INSERT INTO FACTURAS (
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            id_factura,
            id_reservacion,
            numero_factura,
            fecha_factura,
            subtotal,
            impuesto,
            id_descuento,
            total,
            id_estado,
        )
        self.db.execute(query, params)

    def actualizar_factura(
        self,
        id_factura: int,
        id_reservacion: int,
        numero_factura: str,
        fecha_factura: str,
        subtotal: float,
        impuesto: float,
        id_descuento: int | None,
        total: float,
        id_estado: int,
    ) -> None:
        query = """
        UPDATE FACTURAS
        SET
            id_reservacion = ?,
            numero_factura = ?,
            fecha_factura = ?,
            subtotal = ?,
            impuesto = ?,
            id_descuento = ?,
            total = ?,
            id_estado = ?
        WHERE id_factura = ?;
        """
        params = (
            id_reservacion,
            numero_factura,
            fecha_factura,
            subtotal,
            impuesto,
            id_descuento,
            total,
            id_estado,
            id_factura,
        )
        self.db.execute(query, params)

    def eliminar_factura(self, id_factura: int) -> None:
        query = """
        DELETE FROM FACTURAS
        WHERE id_factura = ?;
        """
        self.db.execute(query, (id_factura,))

    def listar_reservaciones(self):
        query = """
        SELECT
            r.id_reservacion,
            c.cedula,
            c.nombre,
            c.apellido1,
            c.apellido2,
            r.total
        FROM RESERVACIONES r
        INNER JOIN CLIENTES c
            ON r.id_cliente = c.id_cliente
        ORDER BY r.id_reservacion;
        """
        return self.db.execute(query, fetch=True)

    def listar_descuentos(self):
        query = """
        SELECT
            id_descuento,
            tipo_descuento
        FROM DESCUENTOS
        ORDER BY tipo_descuento;
        """
        return self.db.execute(query, fetch=True)

    def listar_estados_factura(self):
        query = """
        SELECT
            id_estado,
            estado
        FROM ESTADO_FACTURA
        ORDER BY estado;
        """
        return self.db.execute(query, fetch=True)

    def obtener_montos_reservacion(self, id_reservacion: int):
        query = """
        SELECT
            subtotal,
            impuestos,
            total
        FROM RESERVACIONES
        WHERE id_reservacion = ?;
        """
        return self.db.execute(query, (id_reservacion,), fetch_one=True)