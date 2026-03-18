import tkinter as tk
from tkinter import ttk, messagebox

from core.logger import get_logger
from services.factura_service import FacturaService


logger = get_logger("FacturasView")


class FacturasView(ttk.Frame):
    """
    Vista del módulo de facturas.
    Incluye:
    - formulario
    - combos de catálogos
    - cálculo visual de montos
    - tabla de listado
    - acciones CRUD básicas
    """

    def __init__(self, master) -> None:
        super().__init__(master, style="App.TFrame")
        self.service = FacturaService()

        self.selected_factura_id: int | None = None

        self.reservaciones_map: dict[str, int] = {}
        self.descuentos_map: dict[str, int] = {}
        self.estados_map: dict[str, int] = {}

        self._build_ui()
        self._load_catalogs()
        self._load_facturas()

    # =========================================================
    # UI
    # =========================================================
    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # -----------------------------------------------------
        # Formulario
        # -----------------------------------------------------
        form_card = ttk.Frame(self, style="Surface.TFrame", padding=20)
        form_card.grid(row=0, column=0, sticky="ew", pady=(0, 16))

        for col in range(4):
            form_card.grid_columnconfigure(col, weight=1)

        ttk.Label(form_card, text="Gestión de Facturas", style="Title.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 12)
        )

        # Fila 1
        ttk.Label(form_card, text="Reservación").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        self.combo_reservacion = ttk.Combobox(form_card, state="readonly")
        self.combo_reservacion.grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.combo_reservacion.bind("<<ComboboxSelected>>", self._on_recalcular_total)

        ttk.Label(form_card, text="Número factura").grid(row=1, column=1, sticky="w", padx=8, pady=6)
        self.entry_numero_factura = ttk.Entry(form_card)
        self.entry_numero_factura.grid(row=2, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Fecha factura (YYYY-MM-DD)").grid(
            row=1, column=2, sticky="w", padx=8, pady=6
        )
        self.entry_fecha_factura = ttk.Entry(form_card)
        self.entry_fecha_factura.grid(row=2, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Descuento (opcional)").grid(
            row=1, column=3, sticky="w", padx=(8, 0), pady=6
        )
        self.combo_descuento = ttk.Combobox(form_card, state="readonly")
        self.combo_descuento.grid(row=2, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))
        self.combo_descuento.bind("<<ComboboxSelected>>", self._on_recalcular_total)

        # Fila 2
        ttk.Label(form_card, text="Estado").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=6)
        self.combo_estado = ttk.Combobox(form_card, state="readonly")
        self.combo_estado.grid(row=4, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Subtotal").grid(row=3, column=1, sticky="w", padx=8, pady=6)
        self.entry_subtotal = ttk.Entry(form_card, state="readonly")
        self.entry_subtotal.grid(row=4, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Impuesto").grid(row=3, column=2, sticky="w", padx=8, pady=6)
        self.entry_impuesto = ttk.Entry(form_card, state="readonly")
        self.entry_impuesto.grid(row=4, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Total").grid(row=3, column=3, sticky="w", padx=(8, 0), pady=6)
        self.entry_total = ttk.Entry(form_card, state="readonly")
        self.entry_total.grid(row=4, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        # Botonera
        buttons_frame = ttk.Frame(form_card, style="Surface.TFrame")
        buttons_frame.grid(row=5, column=0, columnspan=4, sticky="ew", pady=(8, 0))

        self.btn_nuevo = ttk.Button(buttons_frame, text="Nuevo", command=self._on_nuevo)
        self.btn_nuevo.pack(side="left", padx=(0, 8))

        self.btn_guardar = ttk.Button(buttons_frame, text="Guardar", command=self._on_guardar)
        self.btn_guardar.pack(side="left", padx=(0, 8))

        self.btn_actualizar = ttk.Button(buttons_frame, text="Actualizar", command=self._on_actualizar)
        self.btn_actualizar.pack(side="left", padx=(0, 8))

        self.btn_eliminar = ttk.Button(buttons_frame, text="Eliminar", command=self._on_eliminar)
        self.btn_eliminar.pack(side="left", padx=(0, 8))

        self.btn_limpiar = ttk.Button(buttons_frame, text="Limpiar", command=self._clear_form)
        self.btn_limpiar.pack(side="left")

        # -----------------------------------------------------
        # Tabla
        # -----------------------------------------------------
        table_card = ttk.Frame(self, style="Surface.TFrame", padding=20)
        table_card.grid(row=1, column=0, sticky="nsew")

        table_card.grid_rowconfigure(1, weight=1)
        table_card.grid_columnconfigure(0, weight=1)

        ttk.Label(table_card, text="Listado de Facturas", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        columns = (
            "id_factura",
            "id_reservacion",
            "numero_factura",
            "fecha_factura",
            "subtotal",
            "impuesto",
            "descuento",
            "total",
            "estado",
        )

        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=14)
        self.tree.grid(row=1, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.heading("id_factura", text="ID")
        self.tree.heading("id_reservacion", text="Reservación")
        self.tree.heading("numero_factura", text="Número")
        self.tree.heading("fecha_factura", text="Fecha")
        self.tree.heading("subtotal", text="Subtotal")
        self.tree.heading("impuesto", text="Impuesto")
        self.tree.heading("descuento", text="Descuento")
        self.tree.heading("total", text="Total")
        self.tree.heading("estado", text="Estado")

        self.tree.column("id_factura", width=70, anchor="center")
        self.tree.column("id_reservacion", width=90, anchor="center")
        self.tree.column("numero_factura", width=120, anchor="center")
        self.tree.column("fecha_factura", width=110, anchor="center")
        self.tree.column("subtotal", width=100, anchor="e")
        self.tree.column("impuesto", width=100, anchor="e")
        self.tree.column("descuento", width=120, anchor="center")
        self.tree.column("total", width=100, anchor="e")
        self.tree.column("estado", width=100, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    # =========================================================
    # CARGAS INICIALES
    # =========================================================
    def _load_catalogs(self) -> None:
        try:
            reservaciones = self.service.listar_reservaciones()
            descuentos = self.service.listar_descuentos()
            estados = self.service.listar_estados_factura()

            self.reservaciones_map = {
                f"{row.id_reservacion} - {row.cedula} - {row.nombre} {row.apellido1} {row.apellido2} - Total {float(row.total):.2f}": row.id_reservacion
                for row in reservaciones
            }
            self.descuentos_map = {
                row.tipo_descuento: row.id_descuento for row in descuentos
            }
            self.estados_map = {
                row.estado: row.id_estado for row in estados
            }

            self.combo_reservacion["values"] = list(self.reservaciones_map.keys())
            self.combo_descuento["values"] = [""] + list(self.descuentos_map.keys())
            self.combo_estado["values"] = list(self.estados_map.keys())

        except Exception as e:
            logger.error(f"Error al cargar catálogos de facturas: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar los catálogos.\n{e}")

    def _load_facturas(self) -> None:
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            facturas = self.service.listar_facturas()

            for row in facturas:
                descuento = row.tipo_descuento if row.tipo_descuento else ""

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row.id_factura,
                        row.id_reservacion,
                        row.numero_factura,
                        str(row.fecha_factura),
                        f"{float(row.subtotal):.2f}",
                        f"{float(row.impuesto):.2f}",
                        descuento,
                        f"{float(row.total):.2f}",
                        row.estado,
                    ),
                )

        except Exception as e:
            logger.error(f"Error al cargar facturas: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el listado de facturas.\n{e}")

    # =========================================================
    # EVENTOS
    # =========================================================
    def _on_nuevo(self) -> None:
        self._clear_form()
        self.combo_reservacion.focus_set()

    def _on_guardar(self) -> None:
        try:
            id_reservacion = self._get_selected_id(
                self.combo_reservacion, self.reservaciones_map, "reservación"
            )
            id_descuento = self._get_selected_descuento_id()
            id_estado = self._get_selected_id(
                self.combo_estado, self.estados_map, "estado"
            )

            nuevo_id = self.service.crear_factura(
                id_reservacion=id_reservacion,
                numero_factura=self.entry_numero_factura.get(),
                fecha_factura=self.entry_fecha_factura.get(),
                id_descuento=id_descuento,
                id_estado=id_estado,
            )

            self._load_facturas()
            self._clear_form()

            messagebox.showinfo(
                "Éxito",
                f"Factura guardada correctamente.\nID asignado: {nuevo_id}"
            )

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al guardar factura: {e}")
            messagebox.showerror("Error", f"No se pudo guardar la factura.\n{e}")

    def _on_actualizar(self) -> None:
        try:
            if self.selected_factura_id is None:
                raise ValueError("Debe seleccionar una factura para actualizar.")

            id_reservacion = self._get_selected_id(
                self.combo_reservacion, self.reservaciones_map, "reservación"
            )
            id_descuento = self._get_selected_descuento_id()
            id_estado = self._get_selected_id(
                self.combo_estado, self.estados_map, "estado"
            )

            self.service.actualizar_factura(
                id_factura=self.selected_factura_id,
                id_reservacion=id_reservacion,
                numero_factura=self.entry_numero_factura.get(),
                fecha_factura=self.entry_fecha_factura.get(),
                id_descuento=id_descuento,
                id_estado=id_estado,
            )

            self._load_facturas()
            self._clear_form()

            messagebox.showinfo("Éxito", "Factura actualizada correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al actualizar factura: {e}")
            messagebox.showerror("Error", f"No se pudo actualizar la factura.\n{e}")

    def _on_eliminar(self) -> None:
        try:
            if self.selected_factura_id is None:
                raise ValueError("Debe seleccionar una factura para eliminar.")

            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                "¿Desea eliminar la factura seleccionada?"
            )
            if not confirm:
                return

            self.service.eliminar_factura(self.selected_factura_id)
            self._load_facturas()
            self._clear_form()

            messagebox.showinfo("Éxito", "Factura eliminada correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al eliminar factura: {e}")
            messagebox.showerror("Error", f"No se pudo eliminar la factura.\n{e}")

    def _on_tree_select(self, event=None) -> None:
        try:
            selected = self.tree.selection()
            if not selected:
                return

            item = self.tree.item(selected[0])
            values = item.get("values", [])
            if not values:
                return

            id_factura = int(values[0])
            factura = self.service.obtener_factura_por_id(id_factura)
            if not factura:
                return

            self.selected_factura_id = factura.id_factura

            self.entry_numero_factura.delete(0, tk.END)
            self.entry_numero_factura.insert(0, factura.numero_factura)

            self.entry_fecha_factura.delete(0, tk.END)
            self.entry_fecha_factura.insert(0, str(factura.fecha_factura))

            self._set_combo_by_id(self.combo_reservacion, self.reservaciones_map, factura.id_reservacion)
            self._set_combo_by_id(self.combo_estado, self.estados_map, factura.id_estado)

            if factura.id_descuento is None:
                self.combo_descuento.set("")
            else:
                self._set_combo_by_id(self.combo_descuento, self.descuentos_map, factura.id_descuento)

            self._recalcular_total()

        except Exception as e:
            logger.error(f"Error al seleccionar factura en la tabla: {e}")
            messagebox.showerror("Error", f"No se pudo cargar la factura seleccionada.\n{e}")

    def _on_recalcular_total(self, event=None) -> None:
        self._recalcular_total()

    # =========================================================
    # HELPERS
    # =========================================================
    def _recalcular_total(self) -> None:
        try:
            reservacion_text = self.combo_reservacion.get().strip()
            if not reservacion_text or reservacion_text not in self.reservaciones_map:
                self._set_readonly_entry(self.entry_subtotal, "")
                self._set_readonly_entry(self.entry_impuesto, "")
                self._set_readonly_entry(self.entry_total, "")
                return

            id_reservacion = self.reservaciones_map[reservacion_text]
            id_descuento = self._get_selected_descuento_id(silent=True)

            subtotal, impuesto, total_base = self.service.obtener_montos_reservacion(id_reservacion)
            total_final = self.service.calcular_total_con_descuento(
                subtotal=subtotal,
                impuesto=impuesto,
                total_base=total_base,
                id_descuento=id_descuento,
            )

            self._set_readonly_entry(self.entry_subtotal, f"{subtotal:.2f}")
            self._set_readonly_entry(self.entry_impuesto, f"{impuesto:.2f}")
            self._set_readonly_entry(self.entry_total, f"{total_final:.2f}")

        except Exception:
            self._set_readonly_entry(self.entry_subtotal, "")
            self._set_readonly_entry(self.entry_impuesto, "")
            self._set_readonly_entry(self.entry_total, "")

    def _set_readonly_entry(self, entry: ttk.Entry, value: str) -> None:
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(state="readonly")

    def _clear_form(self) -> None:
        self.selected_factura_id = None

        self.combo_reservacion.set("")
        self.combo_descuento.set("")
        self.combo_estado.set("")

        self.entry_numero_factura.delete(0, tk.END)
        self.entry_fecha_factura.delete(0, tk.END)

        self._set_readonly_entry(self.entry_subtotal, "")
        self._set_readonly_entry(self.entry_impuesto, "")
        self._set_readonly_entry(self.entry_total, "")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def _get_selected_id(self, combo: ttk.Combobox, mapping: dict[str, int], label: str) -> int:
        selected_text = combo.get().strip()
        if not selected_text:
            raise ValueError(f"Debe seleccionar una {label}.")
        if selected_text not in mapping:
            raise ValueError(f"La {label} seleccionada no es válida.")
        return mapping[selected_text]

    def _get_selected_descuento_id(self, silent: bool = False) -> int | None:
        selected_text = self.combo_descuento.get().strip()
        if not selected_text:
            return None
        if selected_text not in self.descuentos_map:
            if silent:
                return None
            raise ValueError("El descuento seleccionado no es válido.")
        return self.descuentos_map[selected_text]

    def _set_combo_by_id(self, combo: ttk.Combobox, mapping: dict[str, int], target_id: int) -> None:
        for text, value_id in mapping.items():
            if value_id == target_id:
                combo.set(text)
                return
        combo.set("")