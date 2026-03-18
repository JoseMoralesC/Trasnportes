from pathlib import Path


# =========================================================
# RUTAS BASE DEL PROYECTO
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
SQL_DIR = BASE_DIR / "sql"


# =========================================================
# DATOS GENERALES DEL SISTEMA
# =========================================================
APP_NAME = "Sistema de Gestión de Transportes"
APP_VERSION = "1.0.0"


# =========================================================
# CONFIGURACIÓN DE VENTANA PRINCIPAL
# =========================================================
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_MIN_WIDTH = 1100
WINDOW_MIN_HEIGHT = 650


# =========================================================
# CONFIGURACIÓN VISUAL BASE
# =========================================================
SIDEBAR_WIDTH = 240
HEADER_HEIGHT = 60
CONTENT_PADDING = 16


# =========================================================
# COLORES BASE
# =========================================================
COLOR_BG = "#F4F6F8"
COLOR_SURFACE = "#FFFFFF"
COLOR_PRIMARY = "#1F3C88"
COLOR_PRIMARY_HOVER = "#274AA8"
COLOR_ACCENT = "#39A2DB"
COLOR_TEXT = "#1E293B"
COLOR_TEXT_LIGHT = "#64748B"
COLOR_BORDER = "#D9E2EC"
COLOR_SUCCESS = "#16A34A"
COLOR_WARNING = "#D97706"
COLOR_DANGER = "#DC2626"


# =========================================================
# TIPOGRAFÍA BASE
# =========================================================
FONT_FAMILY = "Segoe UI"
FONT_SIZE_TITLE = 16
FONT_SIZE_SUBTITLE = 12
FONT_SIZE_TEXT = 10
FONT_SIZE_SMALL = 9


# =========================================================
# MÓDULOS PRINCIPALES DEL SISTEMA
# =========================================================
MODULES = [
    "Dashboard",
    "Clientes",
    "Empleados",
    "Autobuses",
    "Viajes",
    "Reservaciones",
    "Facturas",
    "Pagos",
]