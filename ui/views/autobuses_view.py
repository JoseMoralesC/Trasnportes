import tkinter as tk
from tkinter import ttk, messagebox

from core.logger import get_logger
from services.autobus_service import AutobusService


logger = get_logger("AutobusesView")


class AutobusesView(ttk.Frame):
    """
    Vista del módulo de autobuses.
    Incluye:
    - formulario
    - combos de catálogos
    - tabla de listado
    - acciones CRUD básicas
    """

    def __init__(self, master) -> None:
        super().__init__(master, style="App.TFrame")
        self.service = AutobusService()

        self.selected_autobus_id: int | None = None

        self.numeros_unidad_map: dict[str, int] = {}
        self.marcas_map: dict[str, int] = {}
        self.modelos_map: dict[str, int] = {}
        self.estados_map: dict[str, int] = {}
        self.tipos_map: dict[str, int] = {}

        self._build_ui()
        self._load_catalogs()
        self._load_autobuses()

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

        ttk.Label(form_card, text="Gestión de Autobuses", style="Title.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 12)
        )

        # Fila 1
        ttk.Label(form_card, text="Placa").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        self.entry_placa = ttk.Entry(form_card)
        self.entry_placa.grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Número de unidad").grid(row=1, column=1, sticky="w", padx=8, pady=6)
        self.combo_num_unidad = ttk.Combobox(form_card, state="readonly")
        self.combo_num_unidad.grid(row=2, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Marca").grid(row=1, column=2, sticky="w", padx=8, pady=6)
        self.combo_marca = ttk.Combobox(form_card, state="readonly")
        self.combo_marca.grid(row=2, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Modelo").grid(row=1, column=3, sticky="w", padx=(8, 0), pady=6)
        self.combo_modelo = ttk.Combobox(form_card, state="readonly")
        self.combo_modelo.grid(row=2, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        # Fila 2
        ttk.Label(form_card, text="Año").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=6)
        self.entry_anio = ttk.Entry(form_card)
        self.entry_anio.grid(row=4, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Capacidad").grid(row=3, column=1, sticky="w", padx=8, pady=6)
        self.entry_capacidad = ttk.Entry(form_card)
        self.entry_capacidad.grid(row=4, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Estado").grid(row=3, column=2, sticky="w", padx=8, pady=6)
        self.combo_estado = ttk.Combobox(form_card, state="readonly")
        self.combo_estado.grid(row=4, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Tipo de autobús").grid(row=3, column=3, sticky="w", padx=(8, 0), pady=6)
        self.combo_tipo = ttk.Combobox(form_card, state="readonly")
        self.combo_tipo.grid(row=4, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

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

        ttk.Label(table_card, text="Listado de Autobuses", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        columns = (
            "id_autobus",
            "placa",
            "unidad",
            "marca",
            "modelo",
            "anio",
            "capacidad",
            "estado",
            "tipo",
        )

        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=14)
        self.tree.grid(row=1, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.heading("id_autobus", text="ID")
        self.tree.heading("placa", text="Placa")
        self.tree.heading("unidad", text="Unidad")
        self.tree.heading("marca", text="Marca")
        self.tree.heading("modelo", text="Modelo")
        self.tree.heading("anio", text="Año")
        self.tree.heading("capacidad", text="Capacidad")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("tipo", text="Tipo")

        self.tree.column("id_autobus", width=70, anchor="center")
        self.tree.column("placa", width=100, anchor="center")
        self.tree.column("unidad", width=100, anchor="center")
        self.tree.column("marca", width=120)
        self.tree.column("modelo", width=100, anchor="center")
        self.tree.column("anio", width=80, anchor="center")
        self.tree.column("capacidad", width=90, anchor="center")
        self.tree.column("estado", width=110, anchor="center")
        self.tree.column("tipo", width=140)

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    # =========================================================
    # CARGAS INICIALES
    # =========================================================
    def _load_catalogs(self) -> None:
        try:
            numeros = self.service.listar_numeros_unidad()
            marcas = self.service.listar_marcas()
            modelos = self.service.listar_modelos()
            estados = self.service.listar_estados()
            tipos = self.service.listar_tipos_autobus()

            self.numeros_unidad_map = {
                row.unidad: row.id_num_unidad for row in numeros
            }
            self.marcas_map = {
                row.marca: row.id_marca for row in marcas
            }
            self.modelos_map = {
                str(row.modelo): row.id_modelo for row in modelos
            }
            self.estados_map = {
                row.estado: row.id_estado for row in estados
            }
            self.tipos_map = {
                row.nombre_tipo: row.id_tipo_autobus for row in tipos
            }

            self.combo_num_unidad["values"] = list(self.numeros_unidad_map.keys())
            self.combo_marca["values"] = list(self.marcas_map.keys())
            self.combo_modelo["values"] = list(self.modelos_map.keys())
            self.combo_estado["values"] = list(self.estados_map.keys())
            self.combo_tipo["values"] = list(self.tipos_map.keys())

        except Exception as e:
            logger.error(f"Error al cargar catálogos de autobuses: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar los catálogos.\n{e}")

    def _load_autobuses(self) -> None:
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            autobuses = self.service.listar_autobuses()

            for row in autobuses:
                self.tree.insert(
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
                    ),
                )

        except Exception as e:
            logger.error(f"Error al cargar autobuses: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el listado de autobuses.\n{e}")

    # =========================================================
    # EVENTOS
    # =========================================================
    def _on_nuevo(self) -> None:
        self._clear_form()
        self.entry_placa.focus_set()

    def _on_guardar(self) -> None:
        try:
            id_num_unidad = self._get_selected_id(
                self.combo_num_unidad, self.numeros_unidad_map, "número de unidad"
            )
            id_marca = self._get_selected_id(
                self.combo_marca, self.marcas_map, "marca"
            )
            id_modelo = self._get_selected_id(
                self.combo_modelo, self.modelos_map, "modelo"
            )
            id_estado = self._get_selected_id(
                self.combo_estado, self.estados_map, "estado"
            )
            id_tipo = self._get_selected_id(
                self.combo_tipo, self.tipos_map, "tipo de autobús"
            )

            anio = int(self.entry_anio.get().strip())
            capacidad = int(self.entry_capacidad.get().strip())

            nuevo_id = self.service.crear_autobus(
                placa=self.entry_placa.get(),
                id_num_unidad=id_num_unidad,
                id_marca=id_marca,
                id_modelo=id_modelo,
                anio=anio,
                capacidad=capacidad,
                id_estado=id_estado,
                id_tipo_autobus=id_tipo,
            )

            self._load_autobuses()
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

            id_num_unidad = self._get_selected_id(
                self.combo_num_unidad, self.numeros_unidad_map, "número de unidad"
            )
            id_marca = self._get_selected_id(
                self.combo_marca, self.marcas_map, "marca"
            )
            id_modelo = self._get_selected_id(
                self.combo_modelo, self.modelos_map, "modelo"
            )
            id_estado = self._get_selected_id(
                self.combo_estado, self.estados_map, "estado"
            )
            id_tipo = self._get_selected_id(
                self.combo_tipo, self.tipos_map, "tipo de autobús"
            )

            anio = int(self.entry_anio.get().strip())
            capacidad = int(self.entry_capacidad.get().strip())

            self.service.actualizar_autobus(
                id_autobus=self.selected_autobus_id,
                placa=self.entry_placa.get(),
                id_num_unidad=id_num_unidad,
                id_marca=id_marca,
                id_modelo=id_modelo,
                anio=anio,
                capacidad=capacidad,
                id_estado=id_estado,
                id_tipo_autobus=id_tipo,
            )

            self._load_autobuses()
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
            self._load_autobuses()
            self._clear_form()

            messagebox.showinfo("Éxito", "Autobús eliminado correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al eliminar autobús: {e}")
            messagebox.showerror("Error", f"No se pudo eliminar el autobús.\n{e}")

    def _on_tree_select(self, event=None) -> None:
        try:
            selected = self.tree.selection()
            if not selected:
                return

            item = self.tree.item(selected[0])
            values = item.get("values", [])
            if not values:
                return

            id_autobus = int(values[0])
            autobus = self.service.obtener_autobus_por_id(id_autobus)
            if not autobus:
                return

            self.selected_autobus_id = autobus.id_autobus

            self.entry_placa.delete(0, tk.END)
            self.entry_placa.insert(0, autobus.placa)

            self.entry_anio.delete(0, tk.END)
            self.entry_anio.insert(0, str(autobus.anio))

            self.entry_capacidad.delete(0, tk.END)
            self.entry_capacidad.insert(0, str(autobus.capacidad))

            self._set_combo_by_id(self.combo_num_unidad, self.numeros_unidad_map, autobus.id_num_unidad)
            self._set_combo_by_id(self.combo_marca, self.marcas_map, autobus.id_marca)
            self._set_combo_by_id(self.combo_modelo, self.modelos_map, autobus.id_modelo)
            self._set_combo_by_id(self.combo_estado, self.estados_map, autobus.id_estado)
            self._set_combo_by_id(self.combo_tipo, self.tipos_map, autobus.id_tipo_autobus)

        except Exception as e:
            logger.error(f"Error al seleccionar autobús en la tabla: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el autobús seleccionado.\n{e}")

    # =========================================================
    # HELPERS
    # =========================================================
    def _clear_form(self) -> None:
        self.selected_autobus_id = None

        self.entry_placa.delete(0, tk.END)
        self.entry_anio.delete(0, tk.END)
        self.entry_capacidad.delete(0, tk.END)

        self.combo_num_unidad.set("")
        self.combo_marca.set("")
        self.combo_modelo.set("")
        self.combo_estado.set("")
        self.combo_tipo.set("")

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