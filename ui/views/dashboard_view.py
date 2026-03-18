from tkinter import ttk

from services.dashboard_service import DashboardService


class DashboardView(ttk.Frame):
    """
    Dashboard real del sistema.
    Muestra indicadores generales obtenidos desde la base de datos.
    """

    def __init__(self, master) -> None:
        super().__init__(master, style="App.TFrame")
        self.service = DashboardService()
        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        resumen = self.service.obtener_resumen()

        # -----------------------------------------------------
        # CABECERA / BIENVENIDA
        # -----------------------------------------------------
        welcome_card = ttk.Frame(self, style="Surface.TFrame", padding=24)
        welcome_card.grid(row=0, column=0, sticky="ew", pady=(0, 16))

        ttk.Label(
            welcome_card,
            text="Bienvenido al Sistema de Gestión de Transportes",
            style="Title.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            welcome_card,
            text="Resumen general del sistema en tiempo real.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(8, 0))

        # -----------------------------------------------------
        # CONTENEDOR DE TARJETAS
        # -----------------------------------------------------
        summary_container = ttk.Frame(self, style="App.TFrame")
        summary_container.grid(row=1, column=0, sticky="nsew")

        for col in range(3):
            summary_container.grid_columnconfigure(col, weight=1)

        cards = [
            {
                "title": "Clientes",
                "value": str(resumen["total_clientes"]),
                "hint": "Personas registradas",
                "theme": "blue",
            },
            {
                "title": "Empleados",
                "value": str(resumen["total_empleados"]),
                "hint": "Personal del sistema",
                "theme": "blue",
            },
            {
                "title": "Autobuses",
                "value": str(resumen["total_autobuses"]),
                "hint": "Unidades registradas",
                "theme": "blue",
            },
            {
                "title": "Viajes",
                "value": str(resumen["total_viajes"]),
                "hint": "Programaciones creadas",
                "theme": "orange",
            },
            {
                "title": "Reservaciones",
                "value": str(resumen["total_reservaciones"]),
                "hint": "Reservas realizadas",
                "theme": "orange",
            },
            {
                "title": "Facturas",
                "value": str(resumen["total_facturas"]),
                "hint": "Facturas generadas",
                "theme": "orange",
            },
            {
                "title": "Pagos",
                "value": str(resumen["total_pagos"]),
                "hint": "Pagos registrados",
                "theme": "green",
            },
            {
                "title": "Total facturado",
                "value": self._format_currency(resumen["total_facturado"]),
                "hint": "Monto facturado acumulado",
                "theme": "green",
            },
            {
                "title": "Total pagado",
                "value": self._format_currency(resumen["total_pagado"]),
                "hint": "Monto pagado acumulado",
                "theme": "green",
            },
        ]

        row = 0
        col = 0

        for card_data in cards:
            card = self._create_stat_card(
                parent=summary_container,
                title=card_data["title"],
                value=card_data["value"],
                hint=card_data["hint"],
                theme=card_data["theme"],
            )
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

            col += 1
            if col > 2:
                col = 0
                row += 1

    # =========================================================
    # HELPERS
    # =========================================================
    def _format_currency(self, value: float) -> str:
        return f"₡ {value:,.2f}"

    def _create_stat_card(
        self,
        parent,
        title: str,
        value: str,
        hint: str,
        theme: str = "blue",
    ) -> ttk.Frame:
        frame_style = {
            "blue": "CardBlue.TFrame",
            "green": "CardGreen.TFrame",
            "orange": "CardOrange.TFrame",
        }.get(theme, "CardBlue.TFrame")

        title_style = {
            "blue": "CardTitleBlue.TLabel",
            "green": "CardTitleGreen.TLabel",
            "orange": "CardTitleOrange.TLabel",
        }.get(theme, "CardTitleBlue.TLabel")

        value_style = {
            "blue": "CardValueBlue.TLabel",
            "green": "CardValueGreen.TLabel",
            "orange": "CardValueOrange.TLabel",
        }.get(theme, "CardValueBlue.TLabel")

        hint_style = {
            "blue": "CardHintBlue.TLabel",
            "green": "CardHintGreen.TLabel",
            "orange": "CardHintOrange.TLabel",
        }.get(theme, "CardHintBlue.TLabel")

        card = ttk.Frame(parent, style=frame_style, padding=20)

        ttk.Label(
            card,
            text=title,
            style=title_style,
        ).pack(anchor="w")

        ttk.Label(
            card,
            text=value,
            style=value_style,
        ).pack(anchor="w", pady=(12, 6))

        ttk.Label(
            card,
            text=hint,
            style=hint_style,
        ).pack(anchor="w")

        return card