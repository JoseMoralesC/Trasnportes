import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from tkcalendar import DateEntry

from core.logger import get_logger
from services.viaje_service import ViajeService


logger = get_logger("ViajesView")


class ViajesView(ttk.Frame):
    """
    Vista del módulo de viajes.
    Incluye:
    - formulario
    - combos de catálogos
    - tabla de listado
    - acciones CRUD básicas
    """

    def __init__(self, master) -> None:
        super().__init__(master, style="App.TFrame")
        self.service = ViajeService()

        self.selected_viaje_id: int | None = None

        self.rutas_map: dict[str, int] = {}
        self.autobuses_map: dict[str, int] = {}
        self.precios_map: dict[str, int] = {}
        self.estados_map: dict[str, int] = {}

        self._build_ui()
        self._load_catalogs()
        self._load_viajes()

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

        ttk.Label(form_card, text="Gestión de Viajes", style="Title.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 12)
        )

        # Fila 1
        ttk.Label(form_card, text="Ruta").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        self.combo_ruta = ttk.Combobox(form_card, state="readonly")
        self.combo_ruta.grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Autobús").grid(row=1, column=1, sticky="w", padx=8, pady=6)
        self.combo_autobus = ttk.Combobox(form_card, state="readonly")
        self.combo_autobus.grid(row=2, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Precio base").grid(row=1, column=2, sticky="w", padx=8, pady=6)
        self.combo_precio = ttk.Combobox(form_card, state="readonly")
        self.combo_precio.grid(row=2, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Estado").grid(row=1, column=3, sticky="w", padx=(8, 0), pady=6)
        self.combo_estado = ttk.Combobox(form_card, state="readonly")
        self.combo_estado.grid(row=2, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        # Fila 2
        ttk.Label(form_card, text="Fecha salida").grid(
            row=3, column=0, sticky="w", padx=(0, 8), pady=6
        )
        self.entry_fecha_salida = DateEntry(
            form_card,
            date_pattern="yyyy-mm-dd",
            state="readonly"
        )
        self.entry_fecha_salida.grid(row=4, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Hora salida").grid(
            row=3, column=1, sticky="w", padx=8, pady=6
        )

        self.combo_hora_salida = ttk.Combobox(form_card, state="readonly")
        self.combo_hora_salida.grid(row=4, column=1, sticky="ew", padx=8, pady=(0, 8))

        self.combo_hora_salida["values"] = [
            "05:00", "05:30",
            "06:00", "06:30",
            "07:00", "07:30",
            "08:00", "08:30",
            "09:00", "09:30",
            "10:00", "10:30",
            "11:00", "11:30",
            "12:00", "12:30",
            "13:00", "13:30",
            "14:00", "14:30",
            "15:00", "15:30",
            "16:00", "16:30",
            "17:00", "17:30",
            "18:00", "18:30",
            "19:00", "19:30",
            "20:00", "20:30",
            "21:00", "21:30",
            "22:00"
        ]

        ttk.Label(form_card, text="Cupo total").grid(row=3, column=2, sticky="w", padx=8, pady=6)
        self.entry_cupo_total = ttk.Entry(form_card)
        self.entry_cupo_total.grid(row=4, column=2, sticky="ew", padx=8, pady=(0, 8))

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

        ttk.Label(table_card, text="Listado de Viajes", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        columns = (
            "id_viaje",
            "ruta",
            "autobus",
            "fecha_salida",
            "hora_salida",
            "precio_base",
            "cupo_total",
            "estado",
        )

        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=14)
        self.tree.grid(row=1, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.heading("id_viaje", text="ID")
        self.tree.heading("ruta", text="Ruta")
        self.tree.heading("autobus", text="Autobús")
        self.tree.heading("fecha_salida", text="Fecha salida")
        self.tree.heading("hora_salida", text="Hora salida")
        self.tree.heading("precio_base", text="Precio base")
        self.tree.heading("cupo_total", text="Cupo total")
        self.tree.heading("estado", text="Estado")

        self.tree.column("id_viaje", width=70, anchor="center")
        self.tree.column("ruta", width=220)
        self.tree.column("autobus", width=110, anchor="center")
        self.tree.column("fecha_salida", width=120, anchor="center")
        self.tree.column("hora_salida", width=110, anchor="center")
        self.tree.column("precio_base", width=100, anchor="center")
        self.tree.column("cupo_total", width=90, anchor="center")
        self.tree.column("estado", width=110, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    # =========================================================
    # CARGAS INICIALES
    # =========================================================
    def _load_catalogs(self) -> None:
        try:
            rutas = self.service.listar_rutas()
            autobuses = self.service.listar_autobuses()
            precios = self.service.listar_precios_base()
            estados = self.service.listar_estados_viaje()

            self.rutas_map = {
                row.nombre_ruta: row.id_ruta for row in rutas
            }
            self.autobuses_map = {
                row.placa: row.id_autobus for row in autobuses
            }
            self.precios_map = {
                f"{row.id_precio} - {row.precio_base}": row.id_precio for row in precios
            }
            self.estados_map = {
                row.estado: row.id_estado for row in estados
            }

            self.combo_ruta["values"] = list(self.rutas_map.keys())
            self.combo_autobus["values"] = list(self.autobuses_map.keys())
            self.combo_precio["values"] = list(self.precios_map.keys())
            self.combo_estado["values"] = list(self.estados_map.keys())

        except Exception as e:
            logger.error(f"Error al cargar catálogos de viajes: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar los catálogos.\n{e}")

    def _load_viajes(self) -> None:
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            viajes = self.service.listar_viajes()

            for row in viajes:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row.id_viaje,
                        row.nombre_ruta,
                        row.placa,
                        str(row.fecha_salida),
                        str(row.hora_salida),
                        row.precio_base,
                        row.cupo_total,
                        row.estado,
                    ),
                )

        except Exception as e:
            logger.error(f"Error al cargar viajes: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el listado de viajes.\n{e}")

    # =========================================================
    # EVENTOS
    # =========================================================
    def _on_nuevo(self) -> None:
        self._clear_form()
        self.combo_ruta.focus_set()

    def _on_guardar(self) -> None:
        try:
            id_ruta = self._get_selected_id(self.combo_ruta, self.rutas_map, "ruta")
            id_autobus = self._get_selected_id(self.combo_autobus, self.autobuses_map, "autobús")
            id_precio = self._get_selected_id(self.combo_precio, self.precios_map, "precio base")
            id_estado = self._get_selected_id(self.combo_estado, self.estados_map, "estado")

            cupo_total_text = self.entry_cupo_total.get().strip()
            if not cupo_total_text:
                raise ValueError("El cupo total es obligatorio.")

            cupo_total = int(cupo_total_text)

            nuevo_id = self.service.crear_viaje(
                id_ruta=id_ruta,
                id_autobus=id_autobus,
                fecha_salida=self.entry_fecha_salida.get(),
                hora_salida=self.combo_hora_salida.get(),
                id_precio=id_precio,
                cupo_total=cupo_total,
                id_estado=id_estado,
            )

            self._load_viajes()
            self._clear_form()

            messagebox.showinfo(
                "Éxito",
                f"Viaje guardado correctamente.\nID asignado: {nuevo_id}"
            )

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al guardar viaje: {e}")
            messagebox.showerror("Error", f"No se pudo guardar el viaje.\n{e}")

    def _on_actualizar(self) -> None:
        try:
            if self.selected_viaje_id is None:
                raise ValueError("Debe seleccionar un viaje para actualizar.")

            id_ruta = self._get_selected_id(self.combo_ruta, self.rutas_map, "ruta")
            id_autobus = self._get_selected_id(self.combo_autobus, self.autobuses_map, "autobús")
            id_precio = self._get_selected_id(self.combo_precio, self.precios_map, "precio base")
            id_estado = self._get_selected_id(self.combo_estado, self.estados_map, "estado")

            cupo_total_text = self.entry_cupo_total.get().strip()
            if not cupo_total_text:
                raise ValueError("El cupo total es obligatorio.")

            cupo_total = int(cupo_total_text)

            self.service.actualizar_viaje(
                id_viaje=self.selected_viaje_id,
                id_ruta=id_ruta,
                id_autobus=id_autobus,
                fecha_salida=self.entry_fecha_salida.get(),
                hora_salida=self.combo_hora_salida.get(),
                id_precio=id_precio,
                cupo_total=cupo_total,
                id_estado=id_estado,
            )

            self._load_viajes()
            self._clear_form()

            messagebox.showinfo("Éxito", "Viaje actualizado correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al actualizar viaje: {e}")
            messagebox.showerror("Error", f"No se pudo actualizar el viaje.\n{e}")

    def _on_eliminar(self) -> None:
        try:
            if self.selected_viaje_id is None:
                raise ValueError("Debe seleccionar un viaje para eliminar.")

            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                "¿Desea eliminar el viaje seleccionado?"
            )
            if not confirm:
                return

            self.service.eliminar_viaje(self.selected_viaje_id)
            self._load_viajes()
            self._clear_form()

            messagebox.showinfo("Éxito", "Viaje eliminado correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al eliminar viaje: {e}")
            messagebox.showerror("Error", f"No se pudo eliminar el viaje.\n{e}")

    def _on_tree_select(self, event=None) -> None:
        try:
            selected = self.tree.selection()
            if not selected:
                return

            item = self.tree.item(selected[0])
            values = item.get("values", [])
            if not values:
                return

            id_viaje = int(values[0])
            viaje = self.service.obtener_viaje_por_id(id_viaje)
            if not viaje:
                return

            self.selected_viaje_id = viaje.id_viaje

            self.entry_fecha_salida.set_date(str(viaje.fecha_salida))

            self.combo_hora_salida.set(str(viaje.hora_salida)[:5])

            self.entry_cupo_total.delete(0, tk.END)
            self.entry_cupo_total.insert(0, str(viaje.cupo_total))

            self._set_combo_by_id(self.combo_ruta, self.rutas_map, viaje.id_ruta)
            self._set_combo_by_id(self.combo_autobus, self.autobuses_map, viaje.id_autobus)
            self._set_combo_by_id(self.combo_precio, self.precios_map, viaje.id_precio)
            self._set_combo_by_id(self.combo_estado, self.estados_map, viaje.id_estado)

        except Exception as e:
            logger.error(f"Error al seleccionar viaje en la tabla: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el viaje seleccionado.\n{e}")

    # =========================================================
    # HELPERS
    # =========================================================
    def _clear_form(self) -> None:
        self.selected_viaje_id = None

        self.combo_ruta.set("")
        self.combo_autobus.set("")
        self.combo_precio.set("")
        self.combo_estado.set("")

        self.entry_fecha_salida.set_date(date.today())
        self.combo_hora_salida.set("")
        self.entry_cupo_total.delete(0, tk.END)

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