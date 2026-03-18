import logging
from pathlib import Path

from config.settings import LOGS_DIR, APP_NAME


# =========================================================
# CREAR CARPETA DE LOGS SI NO EXISTE
# =========================================================
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# CONFIGURACIÓN DEL LOGGER
# =========================================================
LOG_FILE = LOGS_DIR / "system.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def get_logger(name: str = APP_NAME) -> logging.Logger:
    """
    Retorna una instancia de logger para el módulo que lo solicite.
    """
    return logging.getLogger(name)