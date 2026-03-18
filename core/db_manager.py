import pyodbc
from typing import Any, List, Optional

from config.database import build_connection_string
from core.logger import get_logger


logger = get_logger("DBManager")


class DBManager:
    """
    Encapsula la conexión y ejecución de consultas a SQL Server.
    """

    def __init__(self):
        self.connection: Optional[pyodbc.Connection] = None

    # =========================================================
    # CONEXIÓN
    # =========================================================
    def connect(self) -> None:
        try:
            conn_str = build_connection_string()
            self.connection = pyodbc.connect(conn_str)
            logger.info("Conexión a base de datos establecida correctamente.")
        except Exception as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            raise

    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()
            logger.info("Conexión a base de datos cerrada.")

    # =========================================================
    # EJECUCIÓN DE QUERIES
    # =========================================================
    def execute(
        self,
        query: str,
        params: tuple = (),
        fetch: bool = False,
        fetch_one: bool = False
    ) -> Optional[List[Any]]:
        """
        Ejecuta un query SQL.

        :param query: Consulta SQL
        :param params: Parámetros del query
        :param fetch: Si debe retornar múltiples filas
        :param fetch_one: Si debe retornar una fila
        :return: Resultado o None
        """
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)

            if fetch_one:
                result = cursor.fetchone()
                return result

            if fetch:
                result = cursor.fetchall()
                return result

            self.connection.commit()
            return None

        except Exception as e:
            logger.error(f"Error en ejecución SQL: {e}")
            self.connection.rollback()
            raise

    # =========================================================
    # UTILIDADES
    # =========================================================
    def test_connection(self) -> bool:
        """
        Prueba rápida de conexión.
        """
        try:
            self.connect()
            self.disconnect()
            return True
        except Exception:
            return False