import tkinter as tk
from tkinter import ttk, messagebox

from core.logger import get_logger
from services.reservacion_service import ReservacionService


logger = get_logger("ReservacionesView")


class ReservacionesView(ttk.Frame):
    """
    Vista del módulo de reservaciones.
    Incluye:
    - formulario
    - combos de catálogos
    - cálculo de montos
    - tabla de listado
    - acciones CRUD básicas
    """

    def __init__(self, master) -> None:
        super().__init__(master, style="App.TFrame")
        self.service = ReservacionService()

        self.selected_reservacion_id: int | None = None

        self.clientes_map: dict[str, int] = {}
        self.viajes_map: dict[str, int] = {}
        self.empleados_map: dict[str, int] = {}
        self.estados_map: dict[str, int] = {}

        self._build_ui()
        self._load_catalogs()
        self._load_reservaciones()

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

        ttk.Label(form_card, text="Gestión de Reservaciones", style="Title.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 12)
        )

        # Fila 1
        ttk.Label(form_card, text="Cliente").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        self.combo_cliente = ttk.Combobox(form_card, state="readonly")
        self.combo_cliente.grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Viaje").grid(row=1, column=1, sticky="w", padx=8, pady=6)
        self.combo_viaje = ttk.Combobox(form_card, state="readonly")
        self.combo_viaje.grid(row=2, column=1, sticky="ew", padx=8, pady=(0, 8))
        self.combo_viaje.bind("<<ComboboxSelected>>", self._on_recalcular_montos)

        ttk.Label(form_card, text="Empleado administrativo").grid(
            row=1, column=2, sticky="w", padx=8, pady=6
        )
        self.combo_empleado = ttk.Combobox(form_card, state="readonly")
        self.combo_empleado.grid(row=2, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Estado").grid(row=1, column=3, sticky="w", padx=(8, 0), pady=6)
        self.combo_estado = ttk.Combobox(form_card, state="readonly")
        self.combo_estado.grid(row=2, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        # Fila 2
        ttk.Label(form_card, text="Fecha reservación (YYYY-MM-DD)").grid(
            row=3, column=0, sticky="w", padx=(0, 8), pady=6
        )
        self.entry_fecha_reservacion = ttk.Entry(form_card)
        self.entry_fecha_reservacion.grid(row=4, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Cantidad pasajeros").grid(
            row=3, column=1, sticky="w", padx=8, pady=6
        )
        self.entry_cantidad_pasajeros = ttk.Entry(form_card)
        self.entry_cantidad_pasajeros.grid(row=4, column=1, sticky="ew", padx=8, pady=(0, 8))
        self.entry_cantidad_pasajeros.bind("<KeyRelease>", self._on_recalcular_montos)

        ttk.Label(form_card, text="Subtotal").grid(row=3, column=2, sticky="w", padx=8, pady=6)
        self.entry_subtotal = ttk.Entry(form_card, state="readonly")
        self.entry_subtotal.grid(row=4, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Impuestos").grid(row=3, column=3, sticky="w", padx=(8, 0), pady=6)
        self.entry_impuestos = ttk.Entry(form_card, state="readonly")
        self.entry_impuestos.grid(row=4, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        # Fila 3
        ttk.Label(form_card, text="Total").grid(row=5, column=0, sticky="w", padx=(0, 8), pady=6)
        self.entry_total = ttk.Entry(form_card, state="readonly")
        self.entry_total.grid(row=6, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        # Botonera
        buttons_frame = ttk.Frame(form_card, style="Surface.TFrame")
        buttons_frame.grid(row=7, column=0, columnspan=4, sticky="ew", pady=(8, 0))

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

        ttk.Label(table_card, text="Listado de Reservaciones", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        columns = (
            "id_reservacion",
            "cliente",
            "viaje",
            "administrativo",
            "fecha_reservacion",
            "cantidad_pasajeros",
            "subtotal",
            "impuestos",
            "total",
            "estado",
        )

        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=14)
        self.tree.grid(row=1, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.heading("id_reservacion", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("viaje", text="Viaje")
        self.tree.heading("administrativo", text="Administrativo")
        self.tree.heading("fecha_reservacion", text="Fecha reservación")
        self.tree.heading("cantidad_pasajeros", text="Pasajeros")
        self.tree.heading("subtotal", text="Subtotal")
        self.tree.heading("impuestos", text="Impuestos")
        self.tree.heading("total", text="Total")
        self.tree.heading("estado", text="Estado")

        self.tree.column("id_reservacion", width=70, anchor="center")
        self.tree.column("cliente", width=220)
        self.tree.column("viaje", width=220)
        self.tree.column("administrativo", width=180)
        self.tree.column("fecha_reservacion", width=120, anchor="center")
        self.tree.column("cantidad_pasajeros", width=80, anchor="center")
        self.tree.column("subtotal", width=90, anchor="e")
        self.tree.column("impuestos", width=90, anchor="e")
        self.tree.column("total", width=90, anchor="e")
        self.tree.column("estado", width=100, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    # =========================================================
    # CARGAS INICIALES
    # =========================================================
    def _load_catalogs(self) -> None:
        try:
            clientes = self.service.listar_clientes()
            viajes = self.service.listar_viajes()
            empleados = self.service.listar_empleados_administrativos()
            estados = self.service.listar_estados_reservacion()

            self.clientes_map = {
                f"{row.cedula} - {row.nombre} {row.apellido1} {row.apellido2}": row.id_cliente
                for row in clientes
            }
            self.viajes_map = {
                f"{row.id_viaje} - {row.nombre_ruta} - {row.fecha_salida} {str(row.hora_salida)[:5]}": row.id_viaje
                for row in viajes
            }
            self.empleados_map = {
                f"{row.id_empleado} - {row.nombre} {row.apellido1} ({row.nombre_rol})": row.id_empleado
                for row in empleados
            }
            self.estados_map = {
                row.estado: row.id_estado for row in estados
            }

            self.combo_cliente["values"] = list(self.clientes_map.keys())
            self.combo_viaje["values"] = list(self.viajes_map.keys())
            self.combo_empleado["values"] = list(self.empleados_map.keys())
            self.combo_estado["values"] = list(self.estados_map.keys())

        except Exception as e:
            logger.error(f"Error al cargar catálogos de reservaciones: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar los catálogos.\n{e}")

    def _load_reservaciones(self) -> None:
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            reservaciones = self.service.listar_reservaciones()

            for row in reservaciones:
                cliente = f"{row.cedula} - {row.nombre} {row.apellido1} {row.apellido2}"
                viaje = f"{row.id_viaje} - {row.nombre_ruta} - {row.fecha_salida} {str(row.hora_salida)[:5]}"
                administrativo = f"{row.nombre_admin} {row.apellido_admin}"

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row.id_reservacion,
                        cliente,
                        viaje,
                        administrativo,
                        str(row.fecha_reservacion),
                        row.cantidad_pasajeros,
                        f"{float(row.subtotal):.2f}",
                        f"{float(row.impuestos):.2f}",
                        f"{float(row.total):.2f}",
                        row.estado,
                    ),
                )

        except Exception as e:
            logger.error(f"Error al cargar reservaciones: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el listado de reservaciones.\n{e}")

    # =========================================================
    # EVENTOS
    # =========================================================
    def _on_nuevo(self) -> None:
        self._clear_form()
        self.combo_cliente.focus_set()

    def _on_guardar(self) -> None:
        try:
            id_cliente = self._get_selected_id(self.combo_cliente, self.clientes_map, "cliente")
            id_viaje = self._get_selected_id(self.combo_viaje, self.viajes_map, "viaje")
            id_empleado = self._get_selected_id(self.combo_empleado, self.empleados_map, "empleado administrativo")
            id_estado = self._get_selected_id(self.combo_estado, self.estados_map, "estado")

            cantidad_text = self.entry_cantidad_pasajeros.get().strip()
            if not cantidad_text:
                raise ValueError("La cantidad de pasajeros es obligatoria.")

            cantidad_pasajeros = int(cantidad_text)

            nuevo_id = self.service.crear_reservacion(
                id_cliente=id_cliente,
                id_viaje=id_viaje,
                id_administrativo=id_empleado,
                fecha_reservacion=self.entry_fecha_reservacion.get(),
                cantidad_pasajeros=cantidad_pasajeros,
                id_estado=id_estado,
            )

            self._load_reservaciones()
            self._clear_form()

            messagebox.showinfo(
                "Éxito",
                f"Reservación guardada correctamente.\nID asignado: {nuevo_id}"
            )

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al guardar reservación: {e}")
            messagebox.showerror("Error", f"No se pudo guardar la reservación.\n{e}")

    def _on_actualizar(self) -> None:
        try:
            if self.selected_reservacion_id is None:
                raise ValueError("Debe seleccionar una reservación para actualizar.")

            id_cliente = self._get_selected_id(self.combo_cliente, self.clientes_map, "cliente")
            id_viaje = self._get_selected_id(self.combo_viaje, self.viajes_map, "viaje")
            id_empleado = self._get_selected_id(self.combo_empleado, self.empleados_map, "empleado administrativo")
            id_estado = self._get_selected_id(self.combo_estado, self.estados_map, "estado")

            cantidad_text = self.entry_cantidad_pasajeros.get().strip()
            if not cantidad_text:
                raise ValueError("La cantidad de pasajeros es obligatoria.")

            cantidad_pasajeros = int(cantidad_text)

            self.service.actualizar_reservacion(
                id_reservacion=self.selected_reservacion_id,
                id_cliente=id_cliente,
                id_viaje=id_viaje,
                id_administrativo=id_empleado,
                fecha_reservacion=self.entry_fecha_reservacion.get(),
                cantidad_pasajeros=cantidad_pasajeros,
                id_estado=id_estado,
            )

            self._load_reservaciones()
            self._clear_form()

            messagebox.showinfo("Éxito", "Reservación actualizada correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al actualizar reservación: {e}")
            messagebox.showerror("Error", f"No se pudo actualizar la reservación.\n{e}")

    def _on_eliminar(self) -> None:
        try:
            if self.selected_reservacion_id is None:
                raise ValueError("Debe seleccionar una reservación para eliminar.")

            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                "¿Desea eliminar la reservación seleccionada?"
            )
            if not confirm:
                return

            self.service.eliminar_reservacion(self.selected_reservacion_id)
            self._load_reservaciones()
            self._clear_form()

            messagebox.showinfo("Éxito", "Reservación eliminada correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al eliminar reservación: {e}")
            messagebox.showerror("Error", f"No se pudo eliminar la reservación.\n{e}")

    def _on_tree_select(self, event=None) -> None:
        try:
            selected = self.tree.selection()
            if not selected:
                return

            item = self.tree.item(selected[0])
            values = item.get("values", [])
            if not values:
                return

            id_reservacion = int(values[0])
            reservacion = self.service.obtener_reservacion_por_id(id_reservacion)
            if not reservacion:
                return

            self.selected_reservacion_id = reservacion.id_reservacion

            self.entry_fecha_reservacion.delete(0, tk.END)
            self.entry_fecha_reservacion.insert(0, str(reservacion.fecha_reservacion))

            self.entry_cantidad_pasajeros.delete(0, tk.END)
            self.entry_cantidad_pasajeros.insert(0, str(reservacion.cantidad_pasajeros))

            self._set_combo_by_id(self.combo_cliente, self.clientes_map, reservacion.id_cliente)
            self._set_combo_by_id(self.combo_viaje, self.viajes_map, reservacion.id_viaje)
            self._set_combo_by_id(self.combo_empleado, self.empleados_map, reservacion.id_administrativo)
            self._set_combo_by_id(self.combo_estado, self.estados_map, reservacion.id_estado)

            self._recalcular_montos()

        except Exception as e:
            logger.error(f"Error al seleccionar reservación en la tabla: {e}")
            messagebox.showerror("Error", f"No se pudo cargar la reservación seleccionada.\n{e}")

    def _on_recalcular_montos(self, event=None) -> None:
        self._recalcular_montos()

    # =========================================================
    # HELPERS
    # =========================================================
    def _recalcular_montos(self) -> None:
        try:
            viaje_text = self.combo_viaje.get().strip()
            cantidad_text = self.entry_cantidad_pasajeros.get().strip()

            if not viaje_text or viaje_text not in self.viajes_map:
                self._set_readonly_entry(self.entry_subtotal, "")
                self._set_readonly_entry(self.entry_impuestos, "")
                self._set_readonly_entry(self.entry_total, "")
                return

            if not cantidad_text:
                self._set_readonly_entry(self.entry_subtotal, "")
                self._set_readonly_entry(self.entry_impuestos, "")
                self._set_readonly_entry(self.entry_total, "")
                return

            cantidad_pasajeros = int(cantidad_text)
            id_viaje = self.viajes_map[viaje_text]

            subtotal, impuestos, total = self.service.calcular_montos(
                id_viaje=id_viaje,
                cantidad_pasajeros=cantidad_pasajeros,
            )

            self._set_readonly_entry(self.entry_subtotal, f"{subtotal:.2f}")
            self._set_readonly_entry(self.entry_impuestos, f"{impuestos:.2f}")
            self._set_readonly_entry(self.entry_total, f"{total:.2f}")

        except Exception:
            self._set_readonly_entry(self.entry_subtotal, "")
            self._set_readonly_entry(self.entry_impuestos, "")
            self._set_readonly_entry(self.entry_total, "")

    def _set_readonly_entry(self, entry: ttk.Entry, value: str) -> None:
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(state="readonly")

    def _clear_form(self) -> None:
        self.selected_reservacion_id = None

        self.combo_cliente.set("")
        self.combo_viaje.set("")
        self.combo_empleado.set("")
        self.combo_estado.set("")

        self.entry_fecha_reservacion.delete(0, tk.END)
        self.entry_cantidad_pasajeros.delete(0, tk.END)

        self._set_readonly_entry(self.entry_subtotal, "")
        self._set_readonly_entry(self.entry_impuestos, "")
        self._set_readonly_entry(self.entry_total, "")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

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