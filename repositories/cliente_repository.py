from core.db_manager import DBManager


class ClienteRepository:
    """
    Acceso a datos del módulo de clientes.
    Toda consulta SQL relacionada con CLIENTES vive aquí.
    """

    def __init__(self) -> None:
        self.db = DBManager()

    def listar_clientes(self):
        query = """
        SELECT
            c.id_cliente,
            c.cedula,
            c.nombre,
            c.apellido1,
            c.apellido2,
            p.nombre_profesion,
            e.nombre_empresa,
            rs.descripcion_rango,
            c.telefono,
            c.correo,
            c.direccion
        FROM CLIENTES c
        INNER JOIN PROFESIONES p
            ON c.id_profesion = p.id_profesion
        INNER JOIN EMPRESAS e
            ON c.id_empresa = e.id_empresa
        INNER JOIN RANGOS_SALARIALES rs
            ON c.id_rango_salarial = rs.id_rango_salarial
        ORDER BY c.id_cliente;
        """
        return self.db.execute(query, fetch=True)

    def obtener_cliente_por_id(self, id_cliente: int):
        query = """
        SELECT
            id_cliente,
            cedula,
            nombre,
            apellido1,
            apellido2,
            id_profesion,
            id_empresa,
            id_rango_salarial,
            telefono,
            correo,
            direccion
        FROM CLIENTES
        WHERE id_cliente = ?;
        """
        return self.db.execute(query, (id_cliente,), fetch_one=True)

    def existe_cedula(self, cedula: str) -> bool:
        query = """
        SELECT 1
        FROM CLIENTES
        WHERE cedula = ?;
        """
        result = self.db.execute(query, (cedula,), fetch_one=True)
        return result is not None

    def existe_correo(self, correo: str) -> bool:
        query = """
        SELECT 1
        FROM CLIENTES
        WHERE correo = ?;
        """
        result = self.db.execute(query, (correo,), fetch_one=True)
        return result is not None

    def obtener_siguiente_id(self) -> int:
        query = """
        SELECT ISNULL(MAX(id_cliente), 0) + 1
        FROM CLIENTES;
        """
        result = self.db.execute(query, fetch_one=True)
        return int(result[0]) if result else 1

    def insertar_cliente(
        self,
        id_cliente: int,
        cedula: str,
        nombre: str,
        apellido1: str,
        apellido2: str,
        id_profesion: int,
        id_empresa: int,
        id_rango_salarial: int,
        telefono: str,
        correo: str,
        direccion: str,
    ) -> None:
        query = """
        INSERT INTO CLIENTES (
            id_cliente,
            cedula,
            nombre,
            apellido1,
            apellido2,
            id_profesion,
            id_empresa,
            id_rango_salarial,
            telefono,
            correo,
            direccion
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            id_cliente,
            cedula,
            nombre,
            apellido1,
            apellido2,
            id_profesion,
            id_empresa,
            id_rango_salarial,
            telefono,
            correo,
            direccion,
        )
        self.db.execute(query, params)

    def actualizar_cliente(
        self,
        id_cliente: int,
        cedula: str,
        nombre: str,
        apellido1: str,
        apellido2: str,
        id_profesion: int,
        id_empresa: int,
        id_rango_salarial: int,
        telefono: str,
        correo: str,
        direccion: str,
    ) -> None:
        query = """
        UPDATE CLIENTES
        SET
            cedula = ?,
            nombre = ?,
            apellido1 = ?,
            apellido2 = ?,
            id_profesion = ?,
            id_empresa = ?,
            id_rango_salarial = ?,
            telefono = ?,
            correo = ?,
            direccion = ?
        WHERE id_cliente = ?;
        """
        params = (
            cedula,
            nombre,
            apellido1,
            apellido2,
            id_profesion,
            id_empresa,
            id_rango_salarial,
            telefono,
            correo,
            direccion,
            id_cliente,
        )
        self.db.execute(query, params)

    def eliminar_cliente(self, id_cliente: int) -> None:
        query = """
        DELETE FROM CLIENTES
        WHERE id_cliente = ?;
        """
        self.db.execute(query, (id_cliente,))

    def listar_profesiones(self):
        query = """
        SELECT id_profesion, nombre_profesion
        FROM PROFESIONES
        ORDER BY nombre_profesion;
        """
        return self.db.execute(query, fetch=True)

    def listar_empresas(self):
        query = """
        SELECT id_empresa, nombre_empresa
        FROM EMPRESAS
        ORDER BY nombre_empresa;
        """
        return self.db.execute(query, fetch=True)

    def listar_rangos_salariales(self):
        query = """
        SELECT id_rango_salarial, descripcion_rango
        FROM RANGOS_SALARIALES
        ORDER BY id_rango_salarial;
        """
        return self.db.execute(query, fetch=True)