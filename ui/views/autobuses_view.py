from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from core.logger import get_logger
from services.autobus_service import AutobusService


logger = get_logger("AutobusesView")


class AutobusesView(ttk.Frame):
    """
    Vista del módulo de autobuses.
    Incluye:
    - datos del autobús
    - datos actuales de DEKRA
    - datos actuales de MARCHAMO
    """

    def __init__(self, master) -> None:
        super().__init__(master, style="App.TFrame")
        self.service = AutobusService()

        self.selected_autobus_id: int | None = None
        self.selected_id_num_unidad: int | None = None

        self.marcas_map: dict[str, int] = {}
        self.modelos_map: dict[str, int] = {}
        self.estados_map: dict[str, int] = {}
        self.tipos_map: dict[str, int] = {}
        self.estados_dekra_map: dict[str, int] = {}
        self.estados_marchamo_map: dict[str, int] = {}
        self.unidades_selector_map: dict[str, int] = {}

        self._build_ui()
        self._load_catalogs()
        self._load_unidades_selector()
        self._prepare_next_unit()
        self._set_default_dates()
        self._bind_mousewheel()

    # =========================================================
    # UI
    # =========================================================
    def _build_ui(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # =====================================================
        # CONTENEDOR SCROLLEABLE
        # =====================================================
        container = ttk.Frame(self, style="App.TFrame")
        container.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            container,
            highlightthickness=0,
            bd=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar_y.set)

        self.scrollable_frame = ttk.Frame(self.canvas, style="App.TFrame")
        self.scrollable_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind(
            "<Configure>",
            self._on_canvas_configure
        )

        # =====================================================
        # TARJETA PRINCIPAL DEL FORMULARIO
        # =====================================================
        form_card = ttk.Frame(self.scrollable_frame, style="Surface.TFrame", padding=20)
        form_card.pack(fill="x", expand=True, padx=0, pady=(0, 16))

        for col in range(4):
            form_card.grid_columnconfigure(col, weight=1)

        ttk.Label(form_card, text="Gestión de Autobuses", style="Title.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 12)
        )

        # =====================================================
        # SELECTOR DE UNIDAD EXISTENTE
        # =====================================================
        ttk.Label(form_card, text="Seleccionar unidad existente").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=6
        )
        self.combo_unidad_selector = ttk.Combobox(form_card, state="readonly")
        self.combo_unidad_selector.grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=(0, 8), pady=(0, 12)
        )
        self.combo_unidad_selector.bind("<<ComboboxSelected>>", self._on_select_unidad)

        # =====================================================
        # DATOS DEL AUTOBÚS
        # =====================================================
        ttk.Label(form_card, text="Placa").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=6)
        self.entry_placa = ttk.Entry(form_card)
        self.entry_placa.grid(row=4, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Número de unidad").grid(row=3, column=1, sticky="w", padx=8, pady=6)
        self.entry_num_unidad = ttk.Entry(form_card, state="readonly")
        self.entry_num_unidad.grid(row=4, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Marca").grid(row=3, column=2, sticky="w", padx=8, pady=6)
        self.combo_marca = ttk.Combobox(form_card, state="readonly")
        self.combo_marca.grid(row=4, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Modelo").grid(row=3, column=3, sticky="w", padx=(8, 0), pady=6)
        self.combo_modelo = ttk.Combobox(form_card, state="readonly")
        self.combo_modelo.grid(row=4, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        ttk.Label(form_card, text="Año").grid(row=5, column=0, sticky="w", padx=(0, 8), pady=6)
        self.entry_anio = ttk.Entry(form_card)
        self.entry_anio.grid(row=6, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Capacidad").grid(row=5, column=1, sticky="w", padx=8, pady=6)
        self.entry_capacidad = ttk.Entry(form_card)
        self.entry_capacidad.grid(row=6, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Estado").grid(row=5, column=2, sticky="w", padx=8, pady=6)
        self.combo_estado = ttk.Combobox(form_card, state="readonly")
        self.combo_estado.grid(row=6, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Tipo de autobús").grid(row=5, column=3, sticky="w", padx=(8, 0), pady=6)
        self.combo_tipo = ttk.Combobox(form_card, state="readonly")
        self.combo_tipo.grid(row=6, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        # =====================================================
        # BLOQUE DEKRA
        # =====================================================
        ttk.Separator(form_card, orient="horizontal").grid(
            row=7, column=0, columnspan=4, sticky="ew", pady=(12, 12)
        )

        ttk.Label(form_card, text="Datos de DEKRA", style="Subtitle.TLabel").grid(
            row=8, column=0, columnspan=4, sticky="w", pady=(0, 6)
        )

        ttk.Label(form_card, text="Número DEKRA").grid(row=9, column=0, sticky="w", padx=(0, 8), pady=6)
        self.entry_numero_dekra = ttk.Entry(form_card)
        self.entry_numero_dekra.grid(row=10, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Fecha emisión DEKRA").grid(
            row=9, column=1, sticky="w", padx=8, pady=6
        )
        self.entry_fecha_emision_dekra = DateEntry(
            form_card,
            date_pattern="yyyy-mm-dd",
            state="readonly"
        )
        self.entry_fecha_emision_dekra.grid(row=10, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Fecha vencimiento DEKRA").grid(
            row=9, column=2, sticky="w", padx=8, pady=6
        )
        self.entry_fecha_vencimiento_dekra = DateEntry(
            form_card,
            date_pattern="yyyy-mm-dd",
            state="readonly"
        )
        self.entry_fecha_vencimiento_dekra.grid(row=10, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Estado DEKRA").grid(row=9, column=3, sticky="w", padx=(8, 0), pady=6)
        self.combo_estado_dekra = ttk.Combobox(form_card, state="readonly")
        self.combo_estado_dekra.grid(row=10, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        # =====================================================
        # BLOQUE MARCHAMO
        # =====================================================
        ttk.Separator(form_card, orient="horizontal").grid(
            row=11, column=0, columnspan=4, sticky="ew", pady=(12, 12)
        )

        ttk.Label(form_card, text="Datos de MARCHAMO", style="Subtitle.TLabel").grid(
            row=12, column=0, columnspan=4, sticky="w", pady=(0, 6)
        )

        ttk.Label(form_card, text="Número marchamo").grid(row=13, column=0, sticky="w", padx=(0, 8), pady=6)
        self.entry_numero_marchamo = ttk.Entry(form_card)
        self.entry_numero_marchamo.grid(row=14, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Período marchamo").grid(row=13, column=1, sticky="w", padx=8, pady=6)
        self.entry_periodo_marchamo = ttk.Entry(form_card)
        self.entry_periodo_marchamo.grid(row=14, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Fecha pago marchamo").grid(
            row=13, column=2, sticky="w", padx=8, pady=6
        )
        self.entry_fecha_pago_marchamo = DateEntry(
            form_card,
            date_pattern="yyyy-mm-dd",
            state="readonly"
        )
        self.entry_fecha_pago_marchamo.grid(row=14, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Fecha vencimiento marchamo").grid(
            row=13, column=3, sticky="w", padx=(8, 0), pady=6
        )
        self.entry_fecha_vencimiento_marchamo = DateEntry(
            form_card,
            date_pattern="yyyy-mm-dd",
            state="readonly"
        )
        self.entry_fecha_vencimiento_marchamo.grid(row=14, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        ttk.Label(form_card, text="Estado marchamo").grid(row=15, column=0, sticky="w", padx=(0, 8), pady=6)
        self.combo_estado_marchamo = ttk.Combobox(form_card, state="readonly")
        self.combo_estado_marchamo.grid(row=16, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        buttons_frame = ttk.Frame(form_card, style="Surface.TFrame")
        buttons_frame.grid(row=17, column=0, columnspan=4, sticky="ew", pady=(12, 0))

        self.btn_nuevo = ttk.Button(buttons_frame, text="Nuevo", command=self._on_nuevo)
        self.btn_nuevo.pack(side="left", padx=(0, 8))

        self.btn_guardar = ttk.Button(buttons_frame, text="Guardar", command=self._on_guardar)
        self.btn_guardar.pack(side="left", padx=(0, 8))

        self.btn_actualizar = ttk.Button(buttons_frame, text="Actualizar", command=self._on_actualizar)
        self.btn_actualizar.pack(side="left", padx=(0, 8))

        self.btn_eliminar = ttk.Button(buttons_frame, text="Eliminar", command=self._on_eliminar)
        self.btn_eliminar.pack(side="left", padx=(0, 8))

        self.btn_limpiar = ttk.Button(buttons_frame, text="Limpiar", command=self._clear_form)
        self.btn_limpiar.pack(side="left", padx=(0, 8))

        self.btn_lista = ttk.Button(buttons_frame, text="Lista", command=self._on_lista)
        self.btn_lista.pack(side="left")

    def _load_unidades_selector(self) -> None:
        try:
            autobuses = self.service.listar_autobuses()
            self.unidades_selector_map = {
                row.unidad: row.id_autobus for row in autobuses
            }

            if hasattr(self, "combo_unidad_selector"):
                self.combo_unidad_selector["values"] = sorted(self.unidades_selector_map.keys())

        except Exception as e:
            logger.error(f"Error al cargar selector de unidades: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar las unidades.\n{e}")

    # =========================================================
    # CARGAS INICIALES
    # =========================================================
    def _load_catalogs(self) -> None:
        try:
            marcas = self.service.listar_marcas()
            modelos = self.service.listar_modelos()
            estados = self.service.listar_estados()
            tipos = self.service.listar_tipos_autobus()
            estados_dekra = self.service.listar_estados_dekra()
            estados_marchamo = self.service.listar_estados_marchamo()

            self.marcas_map = {row.marca: row.id_marca for row in marcas}
            self.modelos_map = {str(row.modelo): row.id_modelo for row in modelos}
            self.estados_map = {row.estado: row.id_estado for row in estados}
            self.tipos_map = {row.nombre_tipo: row.id_tipo_autobus for row in tipos}
            self.estados_dekra_map = {row.estado: row.id_estado for row in estados_dekra}
            self.estados_marchamo_map = {row.estado: row.id_estado for row in estados_marchamo}

            self.combo_marca["values"] = list(self.marcas_map.keys())
            self.combo_modelo["values"] = list(self.modelos_map.keys())
            self.combo_estado["values"] = list(self.estados_map.keys())
            self.combo_tipo["values"] = list(self.tipos_map.keys())
            self.combo_estado_dekra["values"] = list(self.estados_dekra_map.keys())
            self.combo_estado_marchamo["values"] = list(self.estados_marchamo_map.keys())

        except Exception as e:
            logger.error(f"Error al cargar catálogos de autobuses: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar los catálogos.\n{e}")



    # =========================================================
    # EVENTOS
    # =========================================================
    def _on_nuevo(self) -> None:
        self._clear_form()
        self.entry_placa.focus_set()

    def _on_guardar(self) -> None:
        try:
            id_marca = self._get_selected_id(self.combo_marca, self.marcas_map, "marca")
            id_modelo = self._get_selected_id(self.combo_modelo, self.modelos_map, "modelo")
            id_estado = self._get_selected_id(self.combo_estado, self.estados_map, "estado")
            id_tipo = self._get_selected_id(self.combo_tipo, self.tipos_map, "tipo de autobús")
            id_estado_dekra = self._get_selected_id(
                self.combo_estado_dekra,
                self.estados_dekra_map,
                "estado de DEKRA",
            )
            id_estado_marchamo = self._get_selected_id(
                self.combo_estado_marchamo,
                self.estados_marchamo_map,
                "estado de marchamo",
            )

            anio = int(self.entry_anio.get().strip())
            capacidad = int(self.entry_capacidad.get().strip())

            nuevo_id = self.service.crear_autobus(
                placa=self.entry_placa.get(),
                id_marca=id_marca,
                id_modelo=id_modelo,
                anio=anio,
                capacidad=capacidad,
                id_estado=id_estado,
                id_tipo_autobus=id_tipo,
                numero_dekra=self.entry_numero_dekra.get(),
                fecha_emision_dekra=self.entry_fecha_emision_dekra.get(),
                fecha_vencimiento_dekra=self.entry_fecha_vencimiento_dekra.get(),
                id_estado_dekra=id_estado_dekra,
                numero_marchamo=self.entry_numero_marchamo.get(),
                periodo_marchamo=self.entry_periodo_marchamo.get(),
                fecha_pago_marchamo=self.entry_fecha_pago_marchamo.get(),
                fecha_vencimiento_marchamo=self.entry_fecha_vencimiento_marchamo.get(),
                id_estado_marchamo=id_estado_marchamo,
            )

            self._load_unidades_selector()
            self._clear_form()

            messagebox.showinfo(
                "Éxito",
                f"Autobús guardado correctamente.\nID asignado: {nuevo_id}"
            )

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al guardar autobús: {e}")
            messagebox.showerror("Error", f"No se pudo guardar el autobús.\n{e}")

    def _on_actualizar(self) -> None:
        try:
            if self.selected_autobus_id is None:
                raise ValueError("Debe seleccionar un autobús para actualizar.")

            id_marca = self._get_selected_id(self.combo_marca, self.marcas_map, "marca")
            id_modelo = self._get_selected_id(self.combo_modelo, self.modelos_map, "modelo")
            id_estado = self._get_selected_id(self.combo_estado, self.estados_map, "estado")
            id_tipo = self._get_selected_id(self.combo_tipo, self.tipos_map, "tipo de autobús")
            id_estado_dekra = self._get_selected_id(
                self.combo_estado_dekra,
                self.estados_dekra_map,
                "estado de DEKRA",
            )
            id_estado_marchamo = self._get_selected_id(
                self.combo_estado_marchamo,
                self.estados_marchamo_map,
                "estado de marchamo",
            )

            anio = int(self.entry_anio.get().strip())
            capacidad = int(self.entry_capacidad.get().strip())

            self.service.actualizar_autobus(
                id_autobus=self.selected_autobus_id,
                placa=self.entry_placa.get(),
                id_marca=id_marca,
                id_modelo=id_modelo,
                anio=anio,
                capacidad=capacidad,
                id_estado=id_estado,
                id_tipo_autobus=id_tipo,
                numero_dekra=self.entry_numero_dekra.get(),
                fecha_emision_dekra=self.entry_fecha_emision_dekra.get(),
                fecha_vencimiento_dekra=self.entry_fecha_vencimiento_dekra.get(),
                id_estado_dekra=id_estado_dekra,
                numero_marchamo=self.entry_numero_marchamo.get(),
                periodo_marchamo=self.entry_periodo_marchamo.get(),
                fecha_pago_marchamo=self.entry_fecha_pago_marchamo.get(),
                fecha_vencimiento_marchamo=self.entry_fecha_vencimiento_marchamo.get(),
                id_estado_marchamo=id_estado_marchamo,
            )

            self._load_unidades_selector()            
            self._clear_form()

            messagebox.showinfo("Éxito", "Autobús actualizado correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al actualizar autobús: {e}")
            messagebox.showerror("Error", f"No se pudo actualizar el autobús.\n{e}")

    def _on_eliminar(self) -> None:
        try:
            if self.selected_autobus_id is None:
                raise ValueError("Debe seleccionar un autobús para eliminar.")

            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                "¿Desea eliminar el autobús seleccionado?"
            )
            if not confirm:
                return

            self.service.eliminar_autobus(self.selected_autobus_id)
            self._load_unidades_selector()
            self._clear_form()

            messagebox.showinfo("Éxito", "Autobús eliminado correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al eliminar autobús: {e}")
            messagebox.showerror("Error", f"No se pudo eliminar el autobús.\n{e}")

    def _on_lista(self) -> None:
        try:
            self._abrir_ventana_lista_autobuses()
        except Exception as e:
            logger.error(f"Error al abrir la lista de autobuses: {e}")
            messagebox.showerror("Error", f"No se pudo abrir la lista de autobuses.\n{e}")

    def _on_select_unidad(self, event=None) -> None:
        try:
            unidad = self.combo_unidad_selector.get().strip()
            if not unidad:
                return

            id_autobus = self.unidades_selector_map.get(unidad)
            if not id_autobus:
                return

            self._cargar_autobus_en_formulario(id_autobus)

        except Exception as e:
            logger.error(f"Error al seleccionar unidad desde combo: {e}")
            messagebox.showerror("Error", f"No se pudo cargar la unidad seleccionada.\n{e}")

    def _abrir_ventana_lista_autobuses(self) -> None:
        ventana = tk.Toplevel(self)
        ventana.title("Lista General de Autobuses")
        ventana.geometry("1150x620")
        ventana.minsize(980, 560)
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        main_frame = ttk.Frame(ventana, padding=16, style="Surface.TFrame")
        main_frame.pack(fill="both", expand=True)

        header_frame = ttk.Frame(main_frame, style="Surface.TFrame")
        header_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(
            header_frame,
            text="Lista General de Autobuses",
            style="Title.TLabel"
        ).pack(side="left")

        ttk.Button(
            header_frame,
            text="Cerrar",
            command=ventana.destroy
        ).pack(side="right")

        ttk.Label(
            main_frame,
            text="Vista resumida de las unidades. Seleccione una fila para ver el detalle completo.",
        ).pack(anchor="w", pady=(0, 10))

        table_frame = ttk.Frame(main_frame, style="Surface.TFrame")
        table_frame.pack(fill="both", expand=True, pady=(0, 12))

        columnas = (
            "id",
            "placa",
            "unidad",
            "marca",
            "modelo",
            "anio",
            "capacidad",
            "estado_unidad",
            "tipo",
            "estado_dekra",
            "estado_marchamo",
        )

        tree_lista = ttk.Treeview(
            table_frame,
            columns=columnas,
            show="headings",
            height=14
        )

        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree_lista.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=tree_lista.xview)

        tree_lista.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        tree_lista.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        headings = {
            "id": "ID",
            "placa": "Placa",
            "unidad": "Unidad",
            "marca": "Marca",
            "modelo": "Modelo",
            "anio": "Año",
            "capacidad": "Capacidad",
            "estado_unidad": "Estado Unidad",
            "tipo": "Tipo",
            "estado_dekra": "Estado DEKRA",
            "estado_marchamo": "Estado Marchamo",
        }

        widths = {
            "id": 55,
            "placa": 95,
            "unidad": 80,
            "marca": 110,
            "modelo": 90,
            "anio": 70,
            "capacidad": 80,
            "estado_unidad": 110,
            "tipo": 120,
            "estado_dekra": 115,
            "estado_marchamo": 125,
        }

        centradas = {
            "id", "placa", "unidad", "modelo", "anio", "capacidad"
        }

        for col in columnas:
            tree_lista.heading(col, text=headings[col])
            tree_lista.column(
                col,
                width=widths[col],
                minwidth=widths[col],
                anchor="center" if col in centradas else "w",
                stretch=True,
            )

        detail_card = ttk.LabelFrame(main_frame, text="Detalle del autobús seleccionado", padding=12)
        detail_card.pack(fill="x")

        detail_card.grid_columnconfigure(0, weight=1)
        detail_card.grid_columnconfigure(1, weight=1)
        detail_card.grid_columnconfigure(2, weight=1)
        detail_card.grid_columnconfigure(3, weight=1)

        self.lista_detalle_labels = {
            "numero_dekra": ttk.Label(detail_card, text="N° DEKRA: -"),
            "fecha_emision_dekra": ttk.Label(detail_card, text="Emisión DEKRA: -"),
            "fecha_vencimiento_dekra": ttk.Label(detail_card, text="Vence DEKRA: -"),
            "estado_dekra": ttk.Label(detail_card, text="Estado DEKRA: -"),
            "numero_marchamo": ttk.Label(detail_card, text="N° Marchamo: -"),
            "periodo_marchamo": ttk.Label(detail_card, text="Período marchamo: -"),
            "fecha_pago_marchamo": ttk.Label(detail_card, text="Pago marchamo: -"),
            "fecha_vencimiento_marchamo": ttk.Label(detail_card, text="Vence marchamo: -"),
            "estado_marchamo": ttk.Label(detail_card, text="Estado marchamo: -"),
        }

        self.lista_detalle_labels["numero_dekra"].grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.lista_detalle_labels["fecha_emision_dekra"].grid(row=0, column=1, sticky="w", padx=6, pady=4)
        self.lista_detalle_labels["fecha_vencimiento_dekra"].grid(row=0, column=2, sticky="w", padx=6, pady=4)
        self.lista_detalle_labels["estado_dekra"].grid(row=0, column=3, sticky="w", padx=6, pady=4)

        self.lista_detalle_labels["numero_marchamo"].grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.lista_detalle_labels["periodo_marchamo"].grid(row=1, column=1, sticky="w", padx=6, pady=4)
        self.lista_detalle_labels["fecha_pago_marchamo"].grid(row=1, column=2, sticky="w", padx=6, pady=4)
        self.lista_detalle_labels["fecha_vencimiento_marchamo"].grid(row=1, column=3, sticky="w", padx=6, pady=4)
        self.lista_detalle_labels["estado_marchamo"].grid(row=2, column=0, sticky="w", padx=6, pady=4)

        self._cargar_datos_lista_autobuses(tree_lista)

        tree_lista.bind(
            "<<TreeviewSelect>>",
            lambda event: self._mostrar_detalle_lista_autobuses(tree_lista)
        )

    def _cargar_datos_lista_autobuses(self, tree: ttk.Treeview) -> None:
        for item in tree.get_children():
            tree.delete(item)

        autobuses = self.service.listar_autobuses()

        for row in autobuses:
            tree.insert(
                "",
                "end",
                values=(
                    row.id_autobus,
                    row.placa,
                    row.unidad,
                    row.marca,
                    row.modelo,
                    row.anio,
                    row.capacidad,
                    row.estado_unidad,
                    row.nombre_tipo,
                    row.estado_dekra if row.estado_dekra else "",
                    row.estado_marchamo if row.estado_marchamo else "",
                ),
                tags=(str(row.id_autobus),)
            )           

    def _mostrar_detalle_lista_autobuses(self, tree: ttk.Treeview) -> None:
        seleccion = tree.selection()
        if not seleccion:
            return

        item = tree.item(seleccion[0])
        values = item.get("values", [])
        if not values:
            return

        id_autobus = int(values[0])

        dekra = self.service.obtener_dekra_actual_por_autobus(id_autobus)
        marchamo = self.service.obtener_marchamo_actual_por_autobus(id_autobus)

        self.lista_detalle_labels["numero_dekra"].config(
            text=f"N° DEKRA: {dekra.numero_dekra if dekra else '-'}"
        )
        self.lista_detalle_labels["fecha_emision_dekra"].config(
            text=f"Emisión DEKRA: {str(dekra.fecha_emision) if dekra and dekra.fecha_emision else '-'}"
        )
        self.lista_detalle_labels["fecha_vencimiento_dekra"].config(
            text=f"Vence DEKRA: {str(dekra.fecha_vencimiento) if dekra and dekra.fecha_vencimiento else '-'}"
        )
        self.lista_detalle_labels["estado_dekra"].config(
            text=f"Estado DEKRA: {self._valor_seguro(dekra.estado if dekra and hasattr(dekra, 'estado') else None)}"
        )

        self.lista_detalle_labels["numero_marchamo"].config(
            text=f"N° Marchamo: {marchamo.numero_marchamo if marchamo else '-'}"
        )
        self.lista_detalle_labels["periodo_marchamo"].config(
            text=f"Período marchamo: {marchamo.periodo if marchamo and marchamo.periodo else '-'}"
        )
        self.lista_detalle_labels["fecha_pago_marchamo"].config(
            text=f"Pago marchamo: {str(marchamo.fecha_pago) if marchamo and marchamo.fecha_pago else '-'}"
        )
        self.lista_detalle_labels["fecha_vencimiento_marchamo"].config(
            text=f"Vence marchamo: {str(marchamo.fecha_vencimiento) if marchamo and marchamo.fecha_vencimiento else '-'}"
        )
        self.lista_detalle_labels["estado_marchamo"].config(
            text=f"Estado marchamo: {self._valor_seguro(marchamo.estado if marchamo and hasattr(marchamo, 'estado') else None)}"
        )


    def _cargar_autobus_en_formulario(self, id_autobus: int) -> None:
        autobus = self.service.obtener_autobus_por_id(id_autobus)
        if not autobus:
            return

        dekra = self.service.obtener_dekra_actual_por_autobus(id_autobus)
        marchamo = self.service.obtener_marchamo_actual_por_autobus(id_autobus)

        self.selected_autobus_id = autobus.id_autobus
        self.selected_id_num_unidad = autobus.id_num_unidad

        self.entry_placa.delete(0, tk.END)
        self.entry_placa.insert(0, autobus.placa)

        self.entry_anio.delete(0, tk.END)
        self.entry_anio.insert(0, str(autobus.anio))

        self.entry_capacidad.delete(0, tk.END)
        self.entry_capacidad.insert(0, str(autobus.capacidad))

        unidad_row = self.service.repository.obtener_numero_unidad_por_id(autobus.id_num_unidad)
        unidad_texto = unidad_row.unidad if unidad_row else ""
        self._set_readonly_entry(self.entry_num_unidad, unidad_texto)

        if hasattr(self, "combo_unidad_selector"):
            self.combo_unidad_selector.set(unidad_texto)

        self._set_combo_by_id(self.combo_marca, self.marcas_map, autobus.id_marca)
        self._set_combo_by_id(self.combo_modelo, self.modelos_map, autobus.id_modelo)
        self._set_combo_by_id(self.combo_estado, self.estados_map, autobus.id_estado)
        self._set_combo_by_id(self.combo_tipo, self.tipos_map, autobus.id_tipo_autobus)

        self._set_entry_value(self.entry_numero_dekra, dekra.numero_dekra if dekra else "")
        if dekra and dekra.fecha_emision:
            self.entry_fecha_emision_dekra.set_date(dekra.fecha_emision)
        if dekra and dekra.fecha_vencimiento:
            self.entry_fecha_vencimiento_dekra.set_date(dekra.fecha_vencimiento)
        self._set_combo_by_id(
            self.combo_estado_dekra,
            self.estados_dekra_map,
            dekra.id_estado if dekra else 0,
        )

        self._set_entry_value(self.entry_numero_marchamo, marchamo.numero_marchamo if marchamo else "")
        self._set_entry_value(
            self.entry_periodo_marchamo,
            str(marchamo.periodo) if marchamo and marchamo.periodo else "",
        )
        if marchamo and marchamo.fecha_pago:
            self.entry_fecha_pago_marchamo.set_date(marchamo.fecha_pago)
        if marchamo and marchamo.fecha_vencimiento:
            self.entry_fecha_vencimiento_marchamo.set_date(marchamo.fecha_vencimiento)
        self._set_combo_by_id(
            self.combo_estado_marchamo,
            self.estados_marchamo_map,
            marchamo.id_estado if marchamo else 0,
        )

    # =========================================================
    # HELPERS
    # =========================================================
    def _prepare_next_unit(self) -> None:
        _, unidad = self.service.obtener_siguiente_numero_unidad()
        self._set_readonly_entry(self.entry_num_unidad, unidad)

    def _on_canvas_configure(self, event) -> None:
        self.canvas.itemconfigure(self.scrollable_window, width=event.width) 

    def _bind_mousewheel(self) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _unbind_mousewheel(self) -> None:
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event) -> None:
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def destroy(self):
        self._unbind_mousewheel()
        super().destroy()

    def _set_default_dates(self) -> None:
        hoy = date.today()
        self.entry_fecha_emision_dekra.set_date(hoy)
        self.entry_fecha_vencimiento_dekra.set_date(hoy)
        self.entry_fecha_pago_marchamo.set_date(hoy)
        self.entry_fecha_vencimiento_marchamo.set_date(hoy)        

    def _set_readonly_entry(self, entry: ttk.Entry, value: str) -> None:
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(state="readonly")

    def _set_entry_value(self, entry: ttk.Entry, value: str) -> None:
        entry.delete(0, tk.END)
        entry.insert(0, value)

    def _valor_seguro(self, valor) -> str:
        return str(valor) if valor not in (None, "") else "-"    

    def _clear_form(self) -> None:
        hoy = date.today()

        self.selected_autobus_id = None
        self.selected_id_num_unidad = None

        self.entry_placa.delete(0, tk.END)
        self.entry_anio.delete(0, tk.END)
        self.entry_capacidad.delete(0, tk.END)

        self.entry_numero_dekra.delete(0, tk.END)
        self.entry_fecha_emision_dekra.set_date(hoy)
        self.entry_fecha_vencimiento_dekra.set_date(hoy)

        self.entry_numero_marchamo.delete(0, tk.END)
        self.entry_periodo_marchamo.delete(0, tk.END)
        self.entry_fecha_pago_marchamo.set_date(hoy)
        self.entry_fecha_vencimiento_marchamo.set_date(hoy)

        self.combo_marca.set("")
        self.combo_modelo.set("")
        self.combo_estado.set("")
        self.combo_tipo.set("")
        self.combo_estado_dekra.set("")
        self.combo_estado_marchamo.set("")

        if hasattr(self, "combo_unidad_selector"):
            self.combo_unidad_selector.set("")

        self._prepare_next_unit()


    def _get_selected_id(self, combo: ttk.Combobox, mapping: dict[str, int], label: str) -> int:
        selected_text = combo.get().strip()
        if not selected_text:
            raise ValueError(f"Debe seleccionar un {label}.")
        if selected_text not in mapping:
            raise ValueError(f"El {label} seleccionado no es válido.")
        return mapping[selected_text]

    def _set_combo_by_id(self, combo: ttk.Combobox, mapping: dict[str, int], target_id: int) -> None:
        for text, value_id in mapping.items():
            if value_id == target_id:
                combo.set(text)
                return
        combo.set("")