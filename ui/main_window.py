import tkinter as tk
from tkinter import ttk

from config.settings import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_TEXT,
    SIDEBAR_WIDTH,
)
from core.logger import get_logger
from ui.components.sidebar import Sidebar
from ui.views.dashboard_view import DashboardView
from ui.views.clientes_view import ClientesView
from ui.views.empleados_view import EmpleadosView
from ui.views.autobuses_view import AutobusesView
from ui.views.viajes_view import ViajesView
from ui.views.reservaciones_view import ReservacionesView
from ui.views.facturas_view import FacturasView
from ui.views.pagos_view import PagosView

logger = get_logger("MainWindow")


class MainWindow:
    """
    Ventana principal del sistema.
    Todo el sistema se renderiza dentro de esta única ventana
    para dar sensación de aplicación integrada.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.root.configure(bg=COLOR_BG)

        self.current_view = None

        self._configure_styles()
        self._build_layout()
        self._show_dashboard()

    # =========================================================
    # CONFIGURACIÓN VISUAL GENERAL
    # =========================================================
    def _configure_styles(self) -> None:
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("App.TFrame", background=COLOR_BG)
        style.configure("Surface.TFrame", background=COLOR_SURFACE)
        style.configure(
            "Title.TLabel",
            background=COLOR_SURFACE,
            foreground=COLOR_TEXT,
            font=("Segoe UI", 16, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=COLOR_SURFACE,
            foreground=COLOR_TEXT,
            font=("Segoe UI", 10),
        )
        style.configure(
            "CardBlue.TFrame",
            background="#EAF2FF",
            relief="flat",
        )

        style.configure(
            "CardGreen.TFrame",
            background="#EAFBF1",
            relief="flat",
        )

        style.configure(
            "CardOrange.TFrame",
            background="#FFF4E8",
            relief="flat",
        )

        style.configure(
            "CardTitleBlue.TLabel",
            background="#EAF2FF",
            foreground="#1F3C88",
            font=("Segoe UI", 10, "bold"),
        )

        style.configure(
            "CardTitleGreen.TLabel",
            background="#EAFBF1",
            foreground="#15803D",
            font=("Segoe UI", 10, "bold"),
        )

        style.configure(
            "CardTitleOrange.TLabel",
            background="#FFF4E8",
            foreground="#C2410C",
            font=("Segoe UI", 10, "bold"),
        )

        style.configure(
            "CardValueBlue.TLabel",
            background="#EAF2FF",
            foreground="#1E293B",
            font=("Segoe UI", 20, "bold"),
        )

        style.configure(
            "CardValueGreen.TLabel",
            background="#EAFBF1",
            foreground="#166534",
            font=("Segoe UI", 20, "bold"),
        )

        style.configure(
            "CardValueOrange.TLabel",
            background="#FFF4E8",
            foreground="#9A3412",
            font=("Segoe UI", 20, "bold"),
        )

        style.configure(
            "CardHintBlue.TLabel",
            background="#EAF2FF",
            foreground="#64748B",
            font=("Segoe UI", 9),
        )

        style.configure(
            "CardHintGreen.TLabel",
            background="#EAFBF1",
            foreground="#64748B",
            font=("Segoe UI", 9),
        )

        style.configure(
            "CardHintOrange.TLabel",
            background="#FFF4E8",
            foreground="#64748B",
            font=("Segoe UI", 9),
        )

    # =========================================================
    # ESTRUCTURA PRINCIPAL
    # =========================================================
    def _build_layout(self) -> None:
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = Sidebar(
            master=self.root,
            width=SIDEBAR_WIDTH,
            on_navigate=self._handle_navigation,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        # Contenedor principal derecho
        self.main_container = ttk.Frame(self.root, style="App.TFrame")
        self.main_container.grid(row=0, column=1, sticky="nsew")

        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Header
        self.header_frame = ttk.Frame(self.main_container, style="Surface.TFrame", padding=16)
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.header_title = ttk.Label(
            self.header_frame,
            text="Dashboard",
            style="Title.TLabel"
        )
        self.header_title.pack(anchor="w")

        self.header_subtitle = ttk.Label(
            self.header_frame,
            text="Bienvenido al sistema de gestión de transportes",
            style="Subtitle.TLabel"
        )
        self.header_subtitle.pack(anchor="w", pady=(4, 0))

        # Área de contenido
        self.content_frame = ttk.Frame(self.main_container, style="App.TFrame", padding=16)
        self.content_frame.grid(row=1, column=0, sticky="nsew")

        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    # =========================================================
    # NAVEGACIÓN
    # =========================================================
    def _handle_navigation(self, module_name: str) -> None:
        logger.info(f"Navegación solicitada al módulo: {module_name}")

        if module_name == "Dashboard":
            self._show_dashboard()
            return

        if module_name == "Clientes":
            self._set_header(
                title="Clientes",
                subtitle="Gestión y administración de clientes"
            )
            self._clear_content()
            self.current_view = ClientesView(self.content_frame)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            return
        
        if module_name == "Empleados":
            self._set_header(
                title="Empleados",
                subtitle="Gestion y administración de empleados"
            )
            self._clear_content()
            self.current_view = EmpleadosView(self.content_frame)
            self.current_view.grid(row=0, sticky="nsew")
            return
        
        if module_name == "Autobuses":
            self._set_header(
                title="Autobuses",
                subtitle="Gestión y administración de autobuses"
            )
            self._clear_content()
            self.current_view = AutobusesView(self.content_frame)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            return
        
        if module_name == "Viajes":
            self._set_header(
                title="Viajes",
                subtitle="Gestión y administración de viajes"
            )
            self._clear_content()
            self.current_view = ViajesView(self.content_frame)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            return
        
        if module_name == "Reservaciones":
            self._set_header(
                title="Reservaciones",
                subtitle="Gestión y administracion de reservaciones"
            )
            self._clear_content()
            self.current_view = ReservacionesView(self.content_frame)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            return
        
        if module_name == "Facturas":
            self._set_header(
                title="Facturas",
                subtitle="Gestión y administracion de facturas"
            )
            self._clear_content()
            self.current_view = FacturasView(self.content_frame)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            return
        
        if module_name == "Pagos":
            self._set_header(
                title="Pagos",
                subtitle="Gestión y administracion de pagos"
            )
            self._clear_content()
            self.current_view = PagosView(self.content_frame)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            return

        self._set_header(
            title=module_name,
            subtitle=f"Módulo de {module_name.lower()} en construcción"
        )
        self._clear_content()

        placeholder = ttk.Frame(self.content_frame, style="Surface.TFrame", padding=24)
        placeholder.grid(row=0, column=0, sticky="nsew")

        ttk.Label(
            placeholder,
            text=f"{module_name}",
            style="Title.TLabel"
        ).pack(anchor="center", pady=(20, 10))

        ttk.Label(
            placeholder,
            text="Este módulo será implementado en los siguientes pasos.",
            style="Subtitle.TLabel"
        ).pack(anchor="center")

    def _show_dashboard(self) -> None:
        self._set_header(
            title="Dashboard",
            subtitle="Bienvenido al sistema de gestión de transportes"
        )
        self._clear_content()

        self.current_view = DashboardView(self.content_frame)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    # =========================================================
    # HELPERS DE UI
    # =========================================================
    def _set_header(self, title: str, subtitle: str) -> None:
        self.header_title.config(text=title)
        self.header_subtitle.config(text=subtitle)

    def _clear_content(self) -> None:
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # =========================================================
    # EJECUCIÓN
    # =========================================================
    def run(self) -> None:
        logger.info("Aplicación iniciada correctamente.")
        self.root.mainloop()