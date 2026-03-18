# =========================================================
# CONFIGURACIÓN DE CONEXIÓN A SQL SERVER
# =========================================================

DB_CONFIG = {
    "driver": "ODBC Driver 17 for SQL Server",
    "server": r"TACHER-THR\SQLEXPRESS02",
    "database": "Proyecto1_Transportes",
    "username": "Administrador",
    "password": "1234",
    "trusted_connection": "no",
}


def build_connection_string() -> str:
    """
    Construye el connection string para pyodbc.
    """
    return (
        f"DRIVER={{{DB_CONFIG['driver']}}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        f"TrustServerCertificate=yes;"
    )