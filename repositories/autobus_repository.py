from core.db_manager import DBManager


class AutobusRepository:
    """
    Acceso a datos del módulo de autobuses.
    Toda consulta SQL relacionada con AUTOBUSES vive aquí.
    """

    def __init__(self) -> None:
        self.db = DBManager()

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
            ta.nombre_tipo
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