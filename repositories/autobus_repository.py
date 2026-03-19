from core.db_manager import DBManager


class AutobusRepository:
    """
    Acceso a datos del módulo de autobuses.
    Toda consulta SQL relacionada con AUTOBUSES vive aquí.
    """

    def __init__(self) -> None:
        self.db = DBManager()

    # =========================================================
    # AUTOBUSES
    # =========================================================
    def listar_autobuses(self):
        query = """
        SELECT
            a.id_autobus,
            a.placa,
            nu.unidad,
            mu.marca,
            mo.modelo,
            a.anio,
            a.capacidad,
            eu.estado AS estado_unidad,
            ta.nombre_tipo,
            ISNULL(dk.numero_dekra, '') AS numero_dekra,
            dk.fecha_emision AS dekra_fecha_emision,
            dk.fecha_vencimiento AS dekra_fecha_vencimiento,
            ISNULL(ed.estado, '') AS estado_dekra,
            ISNULL(mh.numero_marchamo, '') AS numero_marchamo,
            mh.periodo AS marchamo_periodo,
            mh.fecha_pago AS marchamo_fecha_pago,
            mh.fecha_vencimiento AS marchamo_fecha_vencimiento,
            ISNULL(em.estado, '') AS estado_marchamo
        FROM AUTOBUSES a
        INNER JOIN NUMERO_UNIDAD nu
            ON a.id_num_unidad = nu.id_num_unidad
        INNER JOIN MARCA_UNIDAD mu
            ON a.id_marca = mu.id_marca
        INNER JOIN MODELO_UNIDAD mo
            ON a.id_modelo = mo.id_modelo
        INNER JOIN ESTADO_UNIDAD eu
            ON a.id_estado = eu.id_estado
        INNER JOIN TIPOS_AUTOBUS ta
            ON a.id_tipo_autobus = ta.id_tipo_autobus
        OUTER APPLY (
            SELECT TOP 1
                d.id_dekra,
                d.numero_dekra,
                d.fecha_emision,
                d.fecha_vencimiento,
                d.id_estado
            FROM DEKRAS d
            WHERE d.id_autobus = a.id_autobus
            ORDER BY d.fecha_vencimiento DESC, d.id_dekra DESC
        ) dk
        LEFT JOIN ESTADO_DEKRA ed
            ON dk.id_estado = ed.id_estado
        OUTER APPLY (
            SELECT TOP 1
                m.id_marchamo,
                m.numero_marchamo,
                m.periodo,
                m.fecha_pago,
                m.fecha_vencimiento,
                m.id_estado
            FROM MARCHAMOS m
            WHERE m.id_autobus = a.id_autobus
            ORDER BY m.fecha_vencimiento DESC, m.id_marchamo DESC
        ) mh
        LEFT JOIN ESTADO_MARCHAMO em
            ON mh.id_estado = em.id_estado
        ORDER BY a.id_autobus;
        """
        return self.db.execute(query, fetch=True)

    def obtener_autobus_por_id(self, id_autobus: int):
        query = """
        SELECT
            id_autobus,
            placa,
            id_num_unidad,
            id_marca,
            id_modelo,
            anio,
            capacidad,
            id_estado,
            id_tipo_autobus
        FROM AUTOBUSES
        WHERE id_autobus = ?;
        """
        return self.db.execute(query, (id_autobus,), fetch_one=True)

    def obtener_numero_unidad_por_id(self, id_num_unidad: int):
        query = """
        SELECT id_num_unidad, unidad
        FROM NUMERO_UNIDAD
        WHERE id_num_unidad = ?;
        """
        return self.db.execute(query, (id_num_unidad,), fetch_one=True)

    def existe_placa(self, placa: str) -> bool:
        query = """
        SELECT 1
        FROM AUTOBUSES
        WHERE placa = ?;
        """
        result = self.db.execute(query, (placa,), fetch_one=True)
        return result is not None

    def obtener_siguiente_id(self) -> int:
        query = """
        SELECT ISNULL(MAX(id_autobus), 0) + 1
        FROM AUTOBUSES;
        """
        result = self.db.execute(query, fetch_one=True)
        return int(result[0]) if result else 1

    def obtener_siguiente_id_num_unidad(self) -> int:
        query = """
        SELECT ISNULL(MAX(id_num_unidad), 0) + 1
        FROM NUMERO_UNIDAD;
        """
        result = self.db.execute(query, fetch_one=True)
        return int(result[0]) if result else 1

    def insertar_numero_unidad(self, id_num_unidad: int, unidad: str) -> None:
        query = """
        INSERT INTO NUMERO_UNIDAD (id_num_unidad, unidad)
        VALUES (?, ?);
        """
        self.db.execute(query, (id_num_unidad, unidad))

    def insertar_autobus(
        self,
        id_autobus: int,
        placa: str,
        id_num_unidad: int,
        id_marca: int,
        id_modelo: int,
        anio: int,
        capacidad: int,
        id_estado: int,
        id_tipo_autobus: int,
    ) -> None:
        query = """
        INSERT INTO AUTOBUSES (
            id_autobus,
            placa,
            id_num_unidad,
            id_marca,
            id_modelo,
            anio,
            capacidad,
            id_estado,
            id_tipo_autobus
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            id_autobus,
            placa,
            id_num_unidad,
            id_marca,
            id_modelo,
            anio,
            capacidad,
            id_estado,
            id_tipo_autobus,
        )
        self.db.execute(query, params)

    def actualizar_autobus(
        self,
        id_autobus: int,
        placa: str,
        id_num_unidad: int,
        id_marca: int,
        id_modelo: int,
        anio: int,
        capacidad: int,
        id_estado: int,
        id_tipo_autobus: int,
    ) -> None:
        query = """
        UPDATE AUTOBUSES
        SET
            placa = ?,
            id_num_unidad = ?,
            id_marca = ?,
            id_modelo = ?,
            anio = ?,
            capacidad = ?,
            id_estado = ?,
            id_tipo_autobus = ?
        WHERE id_autobus = ?;
        """
        params = (
            placa,
            id_num_unidad,
            id_marca,
            id_modelo,
            anio,
            capacidad,
            id_estado,
            id_tipo_autobus,
            id_autobus,
        )
        self.db.execute(query, params)

    def eliminar_autobus(self, id_autobus: int) -> None:
        query = """
        DELETE FROM AUTOBUSES
        WHERE id_autobus = ?;
        """
        self.db.execute(query, (id_autobus,))

    # =========================================================
    # CATÁLOGOS AUTOBÚS
    # =========================================================
    def listar_marcas(self):
        query = """
        SELECT id_marca, marca
        FROM MARCA_UNIDAD
        ORDER BY marca;
        """
        return self.db.execute(query, fetch=True)

    def listar_modelos(self):
        query = """
        SELECT id_modelo, modelo
        FROM MODELO_UNIDAD
        ORDER BY modelo;
        """
        return self.db.execute(query, fetch=True)

    def listar_estados(self):
        query = """
        SELECT id_estado, estado
        FROM ESTADO_UNIDAD
        ORDER BY estado;
        """
        return self.db.execute(query, fetch=True)

    def listar_tipos_autobus(self):
        query = """
        SELECT id_tipo_autobus, nombre_tipo
        FROM TIPOS_AUTOBUS
        ORDER BY nombre_tipo;
        """
        return self.db.execute(query, fetch=True)

    # =========================================================
    # DEKRA
    # =========================================================
    def listar_estados_dekra(self):
        query = """
        SELECT id_estado, estado
        FROM ESTADO_DEKRA
        ORDER BY estado;
        """
        return self.db.execute(query, fetch=True)

    def obtener_dekra_actual_por_autobus(self, id_autobus: int):
        query = """
        SELECT TOP 1
            d.id_dekra,
            d.id_autobus,
            d.numero_dekra,
            d.fecha_emision,
            d.fecha_vencimiento,
            d.id_estado,
            ed.estado
        FROM DEKRAS d
        LEFT JOIN ESTADO_DEKRA ed
            ON d.id_estado = ed.id_estado
        WHERE d.id_autobus = ?
        ORDER BY d.fecha_vencimiento DESC, d.id_dekra DESC;
        """
        return self.db.execute(query, (id_autobus,), fetch_one=True)

    def existe_numero_dekra(self, numero_dekra: str, excluir_id_dekra: int | None = None) -> bool:
        query = """
        SELECT 1
        FROM DEKRAS
        WHERE numero_dekra = ?
          AND (? IS NULL OR id_dekra <> ?);
        """
        result = self.db.execute(
            query,
            (numero_dekra, excluir_id_dekra, excluir_id_dekra),
            fetch_one=True,
        )
        return result is not None

    def obtener_siguiente_id_dekra(self) -> int:
        query = """
        SELECT ISNULL(MAX(id_dekra), 0) + 1
        FROM DEKRAS;
        """
        result = self.db.execute(query, fetch_one=True)
        return int(result[0]) if result else 1

    def insertar_dekra(
        self,
        id_dekra: int,
        id_autobus: int,
        numero_dekra: str,
        fecha_emision: str,
        fecha_vencimiento: str,
        id_estado: int,
    ) -> None:
        query = """
        INSERT INTO DEKRAS (
            id_dekra,
            id_autobus,
            numero_dekra,
            fecha_emision,
            fecha_vencimiento,
            id_estado
        )
        VALUES (?, ?, ?, ?, ?, ?);
        """
        params = (
            id_dekra,
            id_autobus,
            numero_dekra,
            fecha_emision,
            fecha_vencimiento,
            id_estado,
        )
        self.db.execute(query, params)

    def actualizar_dekra(
        self,
        id_dekra: int,
        numero_dekra: str,
        fecha_emision: str,
        fecha_vencimiento: str,
        id_estado: int,
    ) -> None:
        query = """
        UPDATE DEKRAS
        SET
            numero_dekra = ?,
            fecha_emision = ?,
            fecha_vencimiento = ?,
            id_estado = ?
        WHERE id_dekra = ?;
        """
        params = (
            numero_dekra,
            fecha_emision,
            fecha_vencimiento,
            id_estado,
            id_dekra,
        )
        self.db.execute(query, params)

    # =========================================================
    # MARCHAMO
    # =========================================================
    def listar_estados_marchamo(self):
        query = """
        SELECT id_estado, estado
        FROM ESTADO_MARCHAMO
        ORDER BY estado;
        """
        return self.db.execute(query, fetch=True)

    def obtener_marchamo_actual_por_autobus(self, id_autobus: int):
        query = """
        SELECT TOP 1
            m.id_marchamo,
            m.id_autobus,
            m.numero_marchamo,
            m.periodo,
            m.fecha_pago,
            m.fecha_vencimiento,
            m.id_estado,
            em.estado
        FROM MARCHAMOS m
        LEFT JOIN ESTADO_MARCHAMO em
            ON m.id_estado = em.id_estado
        WHERE m.id_autobus = ?
        ORDER BY m.fecha_vencimiento DESC, m.id_marchamo DESC;
        """
        return self.db.execute(query, (id_autobus,), fetch_one=True)

    def existe_numero_marchamo(
        self,
        numero_marchamo: str,
        excluir_id_marchamo: int | None = None,
    ) -> bool:
        query = """
        SELECT 1
        FROM MARCHAMOS
        WHERE numero_marchamo = ?
          AND (? IS NULL OR id_marchamo <> ?);
        """
        result = self.db.execute(
            query,
            (numero_marchamo, excluir_id_marchamo, excluir_id_marchamo),
            fetch_one=True,
        )
        return result is not None

    def existe_marchamo_por_periodo_autobus(
        self,
        id_autobus: int,
        periodo: str,
        excluir_id_marchamo: int | None = None,
    ) -> bool:
        query = """
        SELECT 1
        FROM MARCHAMOS
        WHERE id_autobus = ?
          AND periodo = ?
          AND (? IS NULL OR id_marchamo <> ?);
        """
        result = self.db.execute(
            query,
            (id_autobus, periodo, excluir_id_marchamo, excluir_id_marchamo),
            fetch_one=True,
        )
        return result is not None

    def obtener_siguiente_id_marchamo(self) -> int:
        query = """
        SELECT ISNULL(MAX(id_marchamo), 0) + 1
        FROM MARCHAMOS;
        """
        result = self.db.execute(query, fetch_one=True)
        return int(result[0]) if result else 1

    def insertar_marchamo(
        self,
        id_marchamo: int,
        id_autobus: int,
        numero_marchamo: str,
        periodo: str,
        fecha_pago: str,
        fecha_vencimiento: str,
        id_estado: int,
    ) -> None:
        query = """
        INSERT INTO MARCHAMOS (
            id_marchamo,
            id_autobus,
            numero_marchamo,
            periodo,
            fecha_pago,
            fecha_vencimiento,
            id_estado
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            id_marchamo,
            id_autobus,
            numero_marchamo,
            periodo,
            fecha_pago,
            fecha_vencimiento,
            id_estado,
        )
        self.db.execute(query, params)

    def actualizar_marchamo(
        self,
        id_marchamo: int,
        numero_marchamo: str,
        periodo: str,
        fecha_pago: str,
        fecha_vencimiento: str,
        id_estado: int,
    ) -> None:
        query = """
        UPDATE MARCHAMOS
        SET
            numero_marchamo = ?,
            periodo = ?,
            fecha_pago = ?,
            fecha_vencimiento = ?,
            id_estado = ?
        WHERE id_marchamo = ?;
        """
        params = (
            numero_marchamo,
            periodo,
            fecha_pago,
            fecha_vencimiento,
            id_estado,
            id_marchamo,
        )
        self.db.execute(query, params)