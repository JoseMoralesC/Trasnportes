from core.db_manager import DBManager


class PagoRepository:
    """
    Acceso a datos del módulo de pagos.
    Toda consulta SQL relacionada con PAGOS vive aquí.
    """

    def __init__(self) -> None:
        self.db = DBManager()

    def listar_pagos(self):
        query = """
        SELECT
            p.id_pago,
            p.id_factura,
            f.numero_factura,
            mp.nombre_metodo,
            p.fecha_pago,
            p.monto_pagado,
            p.referencia_pago,
            ep.estado
        FROM PAGOS p
        INNER JOIN FACTURAS f
            ON p.id_factura = f.id_factura
        INNER JOIN METODOS_PAGO mp
            ON p.id_metodo_pago = mp.id_metodo_pago
        INNER JOIN ESTADO_PAGO ep
            ON p.id_estado = ep.id_estado
        ORDER BY p.id_pago;
        """
        return self.db.execute(query, fetch=True)

    def obtener_pago_por_id(self, id_pago: int):
        query = """
        SELECT
            id_pago,
            id_factura,
            id_metodo_pago,
            fecha_pago,
            monto_pagado,
            referencia_pago,
            id_estado
        FROM PAGOS
        WHERE id_pago = ?;
        """
        return self.db.execute(query, (id_pago,), fetch_one=True)

    def existe_referencia_pago(self, referencia_pago: str) -> bool:
        query = """
        SELECT 1
        FROM PAGOS
        WHERE referencia_pago = ?;
        """
        result = self.db.execute(query, (referencia_pago,), fetch_one=True)
        return result is not None

    def obtener_siguiente_id(self) -> int:
        query = """
        SELECT ISNULL(MAX(id_pago), 0) + 1
        FROM PAGOS;
        """
        result = self.db.execute(query, fetch_one=True)
        return int(result[0]) if result else 1

    def insertar_pago(
        self,
        id_pago: int,
        id_factura: int,
        id_metodo_pago: int,
        fecha_pago: str,
        monto_pagado: float,
        referencia_pago: str,
        id_estado: int,
    ) -> None:
        query = """
        INSERT INTO PAGOS (
            id_pago,
            id_factura,
            id_metodo_pago,
            fecha_pago,
            monto_pagado,
            referencia_pago,
            id_estado
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            id_pago,
            id_factura,
            id_metodo_pago,
            fecha_pago,
            monto_pagado,
            referencia_pago,
            id_estado,
        )
        self.db.execute(query, params)

    def actualizar_pago(
        self,
        id_pago: int,
        id_factura: int,
        id_metodo_pago: int,
        fecha_pago: str,
        monto_pagado: float,
        referencia_pago: str,
        id_estado: int,
    ) -> None:
        query = """
        UPDATE PAGOS
        SET
            id_factura = ?,
            id_metodo_pago = ?,
            fecha_pago = ?,
            monto_pagado = ?,
            referencia_pago = ?,
            id_estado = ?
        WHERE id_pago = ?;
        """
        params = (
            id_factura,
            id_metodo_pago,
            fecha_pago,
            monto_pagado,
            referencia_pago,
            id_estado,
            id_pago,
        )
        self.db.execute(query, params)

    def eliminar_pago(self, id_pago: int) -> None:
        query = """
        DELETE FROM PAGOS
        WHERE id_pago = ?;
        """
        self.db.execute(query, (id_pago,))

    def listar_facturas(self):
        query = """
        SELECT
            id_factura,
            numero_factura,
            total
        FROM FACTURAS
        ORDER BY id_factura;
        """
        return self.db.execute(query, fetch=True)

    def listar_metodos_pago(self):
        query = """
        SELECT
            id_metodo_pago,
            nombre_metodo
        FROM METODOS_PAGO
        ORDER BY nombre_metodo;
        """
        return self.db.execute(query, fetch=True)

    def listar_estados_pago(self):
        query = """
        SELECT
            id_estado,
            estado
        FROM ESTADO_PAGO
        ORDER BY estado;
        """
        return self.db.execute(query, fetch=True)

    def obtener_total_factura(self, id_factura: int):
        query = """
        SELECT
            total
        FROM FACTURAS
        WHERE id_factura = ?;
        """
        return self.db.execute(query, (id_factura,), fetch_one=True)