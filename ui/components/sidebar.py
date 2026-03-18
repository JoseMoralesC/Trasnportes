import tkinter as tk
from tkinter import ttk
from typing import Callable

from config.settings import (
    APP_NAME,
    MODULES,
    COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER,
    COLOR_TEXT,
    COLOR_SURFACE,
    COLOR_BG,
    SIDEBAR_WIDTH,
)


class Sidebar(ttk.Frame):
    """
    Menú lateral principal del sistema.
    Permite navegar entre los módulos desde una sola ventana.
    """

    def __init__(
        self,
        master,
        width: int = SIDEBAR_WIDTH,
        on_navigate: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__(master, style="Sidebar.TFrame")

        self.width = width
        self.on_navigate = on_navigate
        self.selected_module = "Dashboard"
        self.buttons: dict[str, tk.Button] = {}

        self._configure_styles()
        self._build_ui()

    # =========================================================
    # ESTILOS
    # =========================================================
    def _configure_styles(self) -> None:
        style = ttk.Style()

        style.configure(
            "Sidebar.TFrame",
            background=COLOR_SURFACE,
        )

        style.configure(
            "SidebarHeader.TFrame",
            background=COLOR_PRIMARY,
        )

        style.configure(
            "SidebarTitle.TLabel",
            background=COLOR_PRIMARY,
            foreground="white",
            font=("Segoe UI", 14, "bold"),
        )

        style.configure(
            "SidebarSubtitle.TLabel",
            background=COLOR_PRIMARY,
            foreground="white",
            font=("Segoe UI", 9),
        )

    # =========================================================
    # UI
    # =========================================================
    def _build_ui(self) -> None:
        self.configure(width=self.width)
        self.grid_propagate(False)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header del sidebar
        header_frame = ttk.Frame(self, style="SidebarHeader.TFrame", padding=16)
        header_frame.grid(row=0, column=0, sticky="ew")

        title_label = ttk.Label(
            header_frame,
            text=APP_NAME,
            style="SidebarTitle.TLabel",
            wraplength=self.width - 32,
            justify="left",
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            header_frame,
            text="Panel principal",
            style="SidebarSubtitle.TLabel",
        )
        subtitle_label.pack(anchor="w", pady=(4, 0))

        # Contenedor de botones
        nav_container = tk.Frame(self, bg=COLOR_SURFACE, highlightthickness=0)
        nav_container.grid(row=1, column=0, sticky="nsew")
        nav_container.grid_columnconfigure(0, weight=1)

        for module_name in MODULES:
            button = tk.Button(
                nav_container,
                text=module_name,
                anchor="w",
                relief="flat",
                bd=0,
                padx=18,
                pady=12,
                font=("Segoe UI", 10, "bold" if module_name == "Dashboard" else "normal"),
                bg=COLOR_BG if module_name == "Dashboard" else COLOR_SURFACE,
                fg=COLOR_PRIMARY if module_name == "Dashboard" else COLOR_TEXT,
                activebackground=COLOR_PRIMARY_HOVER,
                activeforeground="white",
                cursor="hand2",
                command=lambda name=module_name: self._on_click(name),
            )
            button.grid(row=len(self.buttons), column=0, sticky="ew", padx=12, pady=4)
            self.buttons[module_name] = button

        # Footer
        footer = tk.Frame(self, bg=COLOR_SURFACE, highlightthickness=0)
        footer.grid(row=2, column=0, sticky="ew")

        separator = ttk.Separator(footer, orient="horizontal")
        separator.pack(fill="x", padx=12, pady=(8, 8))

        footer_label = tk.Label(
            footer,
            text="Fundamentos de Bases de Datos",
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT,
            font=("Segoe UI", 9),
            anchor="w",
        )
        footer_label.pack(fill="x", padx=16, pady=(0, 12))

    # =========================================================
    # EVENTOS
    # =========================================================
    def _on_click(self, module_name: str) -> None:
        self.selected_module = module_name
        self._refresh_buttons()

        if self.on_navigate:
            self.on_navigate(module_name)

    def _refresh_buttons(self) -> None:
        for module_name, button in self.buttons.items():
            is_selected = module_name == self.selected_module

            button.configure(
                bg=COLOR_BG if is_selected else COLOR_SURFACE,
                fg=COLOR_PRIMARY if is_selected else COLOR_TEXT,
                font=("Segoe UI", 10, "bold" if is_selected else "normal"),
            )