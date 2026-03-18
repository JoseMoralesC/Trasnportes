import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox

from core.logger import get_logger
from tkcalendar import DateEntry
from services.pago_service import PagoService


logger = get_logger("PagosView")


class PagosView(ttk.Frame):
    """
    Vista del módulo de pagos.
    Incluye:
    - formulario
    - combos de catálogos
    - sugerencia de total por factura
    - tabla de listado
    - acciones CRUD básicas
    """

    def __init__(self, master) -> None:
        super().__init__(master, style="App.TFrame")
        self.service = PagoService()

        self.selected_pago_id: int | None = None

        self.facturas_map: dict[str, int] = {}
        self.metodos_map: dict[str, int] = {}
        self.estados_map: dict[str, int] = {}

        self._build_ui()
        self._load_catalogs()
        self._load_pagos()

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

        ttk.Label(form_card, text="Gestión de Pagos", style="Title.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 12)
        )

        # Fila 1
        ttk.Label(form_card, text="Factura").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=6
        )
        self.combo_factura = ttk.Combobox(form_card, state="readonly")
        self.combo_factura.grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))
        self.combo_factura.bind("<<ComboboxSelected>>", self._on_factura_change)

        ttk.Label(form_card, text="Método de pago").grid(
            row=1, column=1, sticky="w", padx=8, pady=6
        )
        self.combo_metodo = ttk.Combobox(form_card, state="readonly")
        self.combo_metodo.grid(row=2, column=1, sticky="ew", padx=8, pady=(0, 8))
        self.combo_metodo.bind("<<ComboboxSelected>>", self._on_metodo_change)

        ttk.Label(form_card, text="Estado").grid(
            row=1, column=2, sticky="w", padx=8, pady=6
        )
        self.combo_estado = ttk.Combobox(form_card, state="readonly")
        self.combo_estado.grid(row=2, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Fecha pago").grid(
            row=1, column=3, sticky="w", padx=(8, 0), pady=6
        )
        self.entry_fecha_pago = DateEntry(
            form_card,
            date_pattern="yyyy-mm-dd",
            state="readonly"
        )
        self.entry_fecha_pago.grid(row=2, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        # Fila 2
        ttk.Label(form_card, text="Monto pagado").grid(
            row=3, column=0, sticky="w", padx=(0, 8), pady=6
        )
        self.entry_monto_pagado = ttk.Entry(form_card)
        self.entry_monto_pagado.grid(row=4, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Referencia pago").grid(
            row=3, column=1, sticky="w", padx=8, pady=6
        )
        self.entry_referencia_pago = ttk.Entry(form_card, state="readonly")
        self.entry_referencia_pago.grid(row=4, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Total factura").grid(
            row=3, column=2, sticky="w", padx=8, pady=6
        )
        self.entry_total_factura = ttk.Entry(form_card, state="readonly")
        self.entry_total_factura.grid(row=4, column=2, sticky="ew", padx=8, pady=(0, 8))

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

        ttk.Label(table_card, text="Listado de Pagos", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        columns = (
            "id_pago",
            "id_factura",
            "numero_factura",
            "metodo",
            "fecha_pago",
            "monto_pagado",
            "referencia_pago",
            "estado",
        )

        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=14)
        self.tree.grid(row=1, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.heading("id_pago", text="ID")
        self.tree.heading("id_factura", text="ID Factura")
        self.tree.heading("numero_factura", text="N° Factura")
        self.tree.heading("metodo", text="Método")
        self.tree.heading("fecha_pago", text="Fecha pago")
        self.tree.heading("monto_pagado", text="Monto")
        self.tree.heading("referencia_pago", text="Referencia")
        self.tree.heading("estado", text="Estado")

        self.tree.column("id_pago", width=70, anchor="center")
        self.tree.column("id_factura", width=90, anchor="center")
        self.tree.column("numero_factura", width=120, anchor="center")
        self.tree.column("metodo", width=130)
        self.tree.column("fecha_pago", width=110, anchor="center")
        self.tree.column("monto_pagado", width=100, anchor="e")
        self.tree.column("referencia_pago", width=180)
        self.tree.column("estado", width=100, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    # =========================================================
    # CARGAS INICIALES
    # =========================================================
    def _load_catalogs(self) -> None:
        try:
            facturas = self.service.listar_facturas()
            metodos = self.service.listar_metodos_pago()
            estados = self.service.listar_estados_pago()

            self.facturas_map = {
                f"{row.id_factura} - {row.numero_factura} - Total {float(row.total):.2f}": row.id_factura
                for row in facturas
            }
            self.metodos_map = {
                row.nombre_metodo: row.id_metodo_pago for row in metodos
            }
            self.estados_map = {
                row.estado: row.id_estado for row in estados
            }

            self.combo_factura["values"] = list(self.facturas_map.keys())
            self.combo_metodo["values"] = list(self.metodos_map.keys())
            self.combo_estado["values"] = list(self.estados_map.keys())

        except Exception as e:
            logger.error(f"Error al cargar catálogos de pagos: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar los catálogos.\n{e}")

    def _load_pagos(self) -> None:
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            pagos = self.service.listar_pagos()

            for row in pagos:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row.id_pago,
                        row.id_factura,
                        row.numero_factura,
                        row.nombre_metodo,
                        str(row.fecha_pago),
                        f"{float(row.monto_pagado):.2f}",
                        row.referencia_pago,
                        row.estado,
                    ),
                )

        except Exception as e:
            logger.error(f"Error al cargar pagos: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el listado de pagos.\n{e}")

    # =========================================================
    # EVENTOS
    # =========================================================
    def _on_nuevo(self) -> None:
        self._clear_form()
        self.combo_factura.focus_set()

    def _on_guardar(self) -> None:
        try:
            id_factura = self._get_selected_id(self.combo_factura, self.facturas_map, "factura")
            id_metodo = self._get_selected_id(self.combo_metodo, self.metodos_map, "método de pago")
            id_estado = self._get_selected_id(self.combo_estado, self.estados_map, "estado")

            monto_text = self.entry_monto_pagado.get().strip()
            if not monto_text:
                raise ValueError("El monto pagado es obligatorio.")

            monto_pagado = float(monto_text)

            nuevo_id = self.service.crear_pago(
                id_factura=id_factura,
                id_metodo_pago=id_metodo,
                fecha_pago=self.entry_fecha_pago.get(),
                monto_pagado=monto_pagado,
                referencia_pago=self.entry_referencia_pago.get(),
                id_estado=id_estado,
            )

            self._load_pagos()
            self._clear_form()

            messagebox.showinfo(
                "Éxito",
                f"Pago guardado correctamente.\nID asignado: {nuevo_id}"
            )

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al guardar pago: {e}")
            messagebox.showerror("Error", f"No se pudo guardar el pago.\n{e}")

    def _on_actualizar(self) -> None:
        try:
            if self.selected_pago_id is None:
                raise ValueError("Debe seleccionar un pago para actualizar.")

            id_factura = self._get_selected_id(self.combo_factura, self.facturas_map, "factura")
            id_metodo = self._get_selected_id(self.combo_metodo, self.metodos_map, "método de pago")
            id_estado = self._get_selected_id(self.combo_estado, self.estados_map, "estado")

            monto_text = self.entry_monto_pagado.get().strip()
            if not monto_text:
                raise ValueError("El monto pagado es obligatorio.")

            monto_pagado = float(monto_text)

            self.service.actualizar_pago(
                id_pago=self.selected_pago_id,
                id_factura=id_factura,
                id_metodo_pago=id_metodo,
                fecha_pago=self.entry_fecha_pago.get(),
                monto_pagado=monto_pagado,
                referencia_pago=self.entry_referencia_pago.get(),
                id_estado=id_estado,
            )

            self._load_pagos()
            self._clear_form()

            messagebox.showinfo("Éxito", "Pago actualizado correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al actualizar pago: {e}")
            messagebox.showerror("Error", f"No se pudo actualizar el pago.\n{e}")

    def _on_eliminar(self) -> None:
        try:
            if self.selected_pago_id is None:
                raise ValueError("Debe seleccionar un pago para eliminar.")

            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                "¿Desea eliminar el pago seleccionado?"
            )
            if not confirm:
                return

            self.service.eliminar_pago(self.selected_pago_id)
            self._load_pagos()
            self._clear_form()

            messagebox.showinfo("Éxito", "Pago eliminado correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al eliminar pago: {e}")
            messagebox.showerror("Error", f"No se pudo eliminar el pago.\n{e}")

    def _on_tree_select(self, event=None) -> None:
        try:
            selected = self.tree.selection()
            if not selected:
                return

            item = self.tree.item(selected[0])
            values = item.get("values", [])
            if not values:
                return

            id_pago = int(values[0])
            pago = self.service.obtener_pago_por_id(id_pago)
            if not pago:
                return

            self.selected_pago_id = pago.id_pago

            self._set_combo_by_id(self.combo_factura, self.facturas_map, pago.id_factura)
            self._set_combo_by_id(self.combo_metodo, self.metodos_map, pago.id_metodo_pago)
            self._set_combo_by_id(self.combo_estado, self.estados_map, pago.id_estado)

            self.entry_fecha_pago.set_date(str(pago.fecha_pago))

            self.entry_monto_pagado.delete(0, tk.END)
            self.entry_monto_pagado.insert(0, str(pago.monto_pagado))

            self._set_readonly_entry(self.entry_referencia_pago, str(pago.referencia_pago))
            self._actualizar_total_factura()

        except Exception as e:
            logger.error(f"Error al seleccionar pago en la tabla: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el pago seleccionado.\n{e}")

    def _on_factura_change(self, event=None) -> None:
        self._actualizar_total_factura()

    def _on_metodo_change(self, event=None) -> None:
        self._actualizar_referencia_pago()

    # =========================================================
    # HELPERS
    # =========================================================
    def _actualizar_total_factura(self) -> None:
        try:
            factura_text = self.combo_factura.get().strip()
            if not factura_text or factura_text not in self.facturas_map:
                self._set_readonly_entry(self.entry_total_factura, "")
                return

            id_factura = self.facturas_map[factura_text]
            total_factura = self.service.obtener_total_factura(id_factura)
            self._set_readonly_entry(self.entry_total_factura, f"{total_factura:.2f}")

        except Exception:
            self._set_readonly_entry(self.entry_total_factura, "")

    def _actualizar_referencia_pago(self) -> None:
        try:
            metodo_text = self.combo_metodo.get().strip()
            if not metodo_text or metodo_text not in self.metodos_map:
                self._set_readonly_entry(self.entry_referencia_pago, "")
                return

            id_metodo = self.metodos_map[metodo_text]

            # Si está editando un pago existente, se conserva la referencia actual
            # siempre que el método no haya cambiado realmente desde la carga.
            if self.selected_pago_id is not None:
                pago_actual = self.service.obtener_pago_por_id(self.selected_pago_id)
                if pago_actual and int(pago_actual.id_metodo_pago) == int(id_metodo):
                    self._set_readonly_entry(
                        self.entry_referencia_pago,
                        str(pago_actual.referencia_pago)
                    )
                    return

            referencia = self.service.generar_referencia_pago(id_metodo)
            self._set_readonly_entry(self.entry_referencia_pago, referencia)

        except Exception:
            self._set_readonly_entry(self.entry_referencia_pago, "")

    def _set_readonly_entry(self, entry: ttk.Entry, value: str) -> None:
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(state="readonly")

    def _clear_form(self) -> None:
        self.selected_pago_id = None

        self.combo_factura.set("")
        self.combo_metodo.set("")
        self.combo_estado.set("")

        self.entry_fecha_pago.set_date(date.today())
        self.entry_monto_pagado.delete(0, tk.END)

        self._set_readonly_entry(self.entry_referencia_pago, "")
        self._set_readonly_entry(self.entry_total_factura, "")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def _get_selected_id(self, combo: ttk.Combobox, mapping: dict[str, int], label: str) -> int:
        selected_text = combo.get().strip()
        if not selected_text:
            raise ValueError(f"Debe seleccionar una {label}.")
        if selected_text not in mapping:
            raise ValueError(f"La {label} seleccionada no es válida.")
        return mapping[selected_text]

    def _set_combo_by_id(self, combo: ttk.Combobox, mapping: dict[str, int], target_id: int) -> None:
        for text, value_id in mapping.items():
            if value_id == target_id:
                combo.set(text)
                return
        combo.set("")