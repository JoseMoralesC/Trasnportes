from core.db_manager import DBManager


class EmpleadoRepository:
    """
    Acceso a datos del módulo de empleados.
    Toda consulta SQL relacionada con EMPLEADOS vive aquí.
    """

    def __init__(self) -> None:
        self.db = DBManager()

    def listar_empleados(self):
        query = """
        SELECT
            e.id_empleado,
            e.cedula,
            e.nombre,
            e.apellido1,
            e.apellido2,
            e.telefono,
            e.correo,
            e.fecha_ingreso,
            r.nombre_rol,
            l.tipo_licencia
        FROM EMPLEADOS e
        INNER JOIN ROLES_EMPLEADO r
            ON e.id_rol = r.id_rol
        LEFT JOIN LICENCIAS_CONDUCIR l
            ON e.id_licencia = l.id_licencia
        ORDER BY e.id_empleado;
        """
        return self.db.execute(query, fetch=True)

    def obtener_empleado_por_id(self, id_empleado: int):
        query = """
        SELECT
            id_empleado,
            cedula,
            nombre,
            apellido1,
            apellido2,
            telefono,
            correo,
            fecha_ingreso,
            id_rol,
            id_licencia
        FROM EMPLEADOS
        WHERE id_empleado = ?;
        """
        return self.db.execute(query, (id_empleado,), fetch_one=True)

    def existe_cedula(self, cedula: str) -> bool:
        query = """
        SELECT 1
        FROM EMPLEADOS
        WHERE cedula = ?;
        """
        result = self.db.execute(query, (cedula,), fetch_one=True)
        return result is not None

    def existe_correo(self, correo: str) -> bool:
        query = """
        SELECT 1
        FROM EMPLEADOS
        WHERE correo = ?;
        """
        result = self.db.execute(query, (correo,), fetch_one=True)
        return result is not None

    def obtener_siguiente_id(self) -> int:
        query = """
        SELECT ISNULL(MAX(id_empleado), 0) + 1
        FROM EMPLEADOS;
        """
        result = self.db.execute(query, fetch_one=True)
        return int(result[0]) if result else 1

    def insertar_empleado(
        self,
        id_empleado: int,
        cedula: str,
        nombre: str,
        apellido1: str,
        apellido2: str,
        telefono: str,
        correo: str,
        fecha_ingreso: str,
        id_rol: int,
        id_licencia: int | None,
    ) -> None:
        query = """
        INSERT INTO EMPLEADOS (
            id_empleado,
            cedula,
            nombre,
            apellido1,
            apellido2,
            telefono,
            correo,
            fecha_ingreso,
            id_rol,
            id_licencia
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            id_empleado,
            cedula,
            nombre,
            apellido1,
            apellido2,
            telefono,
            correo,
            fecha_ingreso,
            id_rol,
            id_licencia,
        )
        self.db.execute(query, params)

    def actualizar_empleado(
        self,
        id_empleado: int,
        cedula: str,
        nombre: str,
        apellido1: str,
        apellido2: str,
        telefono: str,
        correo: str,
        fecha_ingreso: str,
        id_rol: int,
        id_licencia: int | None,
    ) -> None:
        query = """
        UPDATE EMPLEADOS
        SET
            cedula = ?,
            nombre = ?,
            apellido1 = ?,
            apellido2 = ?,
            telefono = ?,
            correo = ?,
            fecha_ingreso = ?,
            id_rol = ?,
            id_licencia = ?
        WHERE id_empleado = ?;
        """
        params = (
            cedula,
            nombre,
            apellido1,
            apellido2,
            telefono,
            correo,
            fecha_ingreso,
            id_rol,
            id_licencia,
            id_empleado,
        )
        self.db.execute(query, params)

    def eliminar_empleado(self, id_empleado: int) -> None:
        query = """
        DELETE FROM EMPLEADOS
        WHERE id_empleado = ?;
        """
        self.db.execute(query, (id_empleado,))

    def listar_roles(self):
        query = """
        SELECT id_rol, nombre_rol
        FROM ROLES_EMPLEADO
        ORDER BY nombre_rol;
        """
        return self.db.execute(query, fetch=True)

    def listar_licencias(self):
        query = """
        SELECT id_licencia, tipo_licencia
        FROM LICENCIAS_CONDUCIR
        ORDER BY tipo_licencia;
        """
        return self.db.execute(query, fetch=True)