# config/database.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = Path(__file__).resolve().parent / "db_config.json"


DEFAULT_DB_CONFIG: Dict[str, Any] = {
    "mode": "sql",  # "sql" o "windows"
    "driver": "ODBC Driver 17 for SQL Server",
    "server": r"localhost\SQLEXPRESS",
    "database": "Proyecto1_Transportes",
    "username": "",
    "password": "",
    "trusted_connection": "yes",
    "trust_server_certificate": "yes",
}


def load_db_config() -> Dict[str, Any]:
    """
    Carga la configuración de base de datos desde db_config.json.
    Si el archivo no existe o está incompleto, rellena con valores por defecto.
    """
    config = DEFAULT_DB_CONFIG.copy()

    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            user_config = json.load(f)
            config.update(user_config)

    return config


def build_connection_string() -> str:
    """
    Construye el connection string para pyodbc según el modo configurado:
    - sql
    - windows
    """
    config = load_db_config()

    driver = config["driver"]
    server = config["server"]
    database = config["database"]
    mode = str(config.get("mode", "sql")).strip().lower()
    trust_server_certificate = config.get("trust_server_certificate", "yes")

    connection_parts = [
        f"DRIVER={{{driver}}}",
        f"SERVER={server}",
        f"DATABASE={database}",
        f"TrustServerCertificate={trust_server_certificate}",
    ]

    if mode == "windows":
        connection_parts.append("Trusted_Connection=yes")
    else:
        username = config.get("username", "")
        password = config.get("password", "")

        if not username or not password:
            raise ValueError(
                "Modo SQL seleccionado, pero faltan 'username' y/o 'password' en db_config.json."
            )

        connection_parts.append(f"UID={username}")
        connection_parts.append(f"PWD={password}")

    return ";".join(connection_parts) + ";"


def get_db_config() -> Dict[str, Any]:
    """
    Retorna la configuración cargada.
    """
    return load_db_config()