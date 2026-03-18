import tkinter as tk
from tkinter import ttk, messagebox

from core.logger import get_logger
from services.empleado_service import EmpleadoService


logger = get_logger("EmpleadosView")


class EmpleadosView(ttk.Frame):
    """
    Vista del módulo de empleados.
    Incluye:
    - formulario
    - combos de catálogos
    - tabla de listado
    - acciones CRUD básicas
    """

    def __init__(self, master) -> None:
        super().__init__(master, style="App.TFrame")
        self.service = EmpleadoService()

        self.selected_empleado_id: int | None = None

        self.roles_map: dict[str, int] = {}
        self.licencias_map: dict[str, int] = {}

        self._build_ui()
        self._load_catalogs()
        self._load_empleados()

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

        ttk.Label(form_card, text="Gestión de Empleados", style="Title.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 12)
        )

        # Fila 1
        ttk.Label(form_card, text="Cédula").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        self.entry_cedula = ttk.Entry(form_card)
        self.entry_cedula.grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Nombre").grid(row=1, column=1, sticky="w", padx=8, pady=6)
        self.entry_nombre = ttk.Entry(form_card)
        self.entry_nombre.grid(row=2, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Primer apellido").grid(row=1, column=2, sticky="w", padx=8, pady=6)
        self.entry_apellido1 = ttk.Entry(form_card)
        self.entry_apellido1.grid(row=2, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Segundo apellido").grid(row=1, column=3, sticky="w", padx=(8, 0), pady=6)
        self.entry_apellido2 = ttk.Entry(form_card)
        self.entry_apellido2.grid(row=2, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        # Fila 2
        ttk.Label(form_card, text="Teléfono").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=6)
        self.entry_telefono = ttk.Entry(form_card)
        self.entry_telefono.grid(row=4, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Correo").grid(row=3, column=1, sticky="w", padx=8, pady=6)
        self.entry_correo = ttk.Entry(form_card)
        self.entry_correo.grid(row=4, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Fecha ingreso (YYYY-MM-DD)").grid(
            row=3, column=2, sticky="w", padx=8, pady=6
        )
        self.entry_fecha_ingreso = ttk.Entry(form_card)
        self.entry_fecha_ingreso.grid(row=4, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Rol").grid(row=3, column=3, sticky="w", padx=(8, 0), pady=6)
        self.combo_rol = ttk.Combobox(form_card, state="readonly")
        self.combo_rol.grid(row=4, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        # Fila 3
        ttk.Label(form_card, text="Licencia (opcional)").grid(row=5, column=0, sticky="w", padx=(0, 8), pady=6)
        self.combo_licencia = ttk.Combobox(form_card, state="readonly")
        self.combo_licencia.grid(row=6, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

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

        ttk.Label(table_card, text="Listado de Empleados", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        columns = (
            "id_empleado",
            "cedula",
            "nombre_completo",
            "telefono",
            "correo",
            "fecha_ingreso",
            "rol",
            "licencia",
        )

        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=14)
        self.tree.grid(row=1, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.heading("id_empleado", text="ID")
        self.tree.heading("cedula", text="Cédula")
        self.tree.heading("nombre_completo", text="Nombre completo")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("fecha_ingreso", text="Fecha ingreso")
        self.tree.heading("rol", text="Rol")
        self.tree.heading("licencia", text="Licencia")

        self.tree.column("id_empleado", width=70, anchor="center")
        self.tree.column("cedula", width=110, anchor="center")
        self.tree.column("nombre_completo", width=220)
        self.tree.column("telefono", width=110, anchor="center")
        self.tree.column("correo", width=180)
        self.tree.column("fecha_ingreso", width=120, anchor="center")
        self.tree.column("rol", width=130)
        self.tree.column("licencia", width=100, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    # =========================================================
    # CARGAS INICIALES
    # =========================================================
    def _load_catalogs(self) -> None:
        try:
            roles = self.service.listar_roles()
            licencias = self.service.listar_licencias()

            self.roles_map = {
                row.nombre_rol: row.id_rol for row in roles
            }
            self.licencias_map = {
                row.tipo_licencia: row.id_licencia for row in licencias
            }

            licencia_values = [""] + list(self.licencias_map.keys())

            self.combo_rol["values"] = list(self.roles_map.keys())
            self.combo_licencia["values"] = licencia_values

        except Exception as e:
            logger.error(f"Error al cargar catálogos de empleados: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar los catálogos.\n{e}")

    def _load_empleados(self) -> None:
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            empleados = self.service.listar_empleados()

            for row in empleados:
                nombre_completo = f"{row.nombre} {row.apellido1} {row.apellido2}"
                licencia = row.tipo_licencia if row.tipo_licencia else ""

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row.id_empleado,
                        row.cedula,
                        nombre_completo,
                        row.telefono,
                        row.correo,
                        str(row.fecha_ingreso),
                        row.nombre_rol,
                        licencia,
                    ),
                )

        except Exception as e:
            logger.error(f"Error al cargar empleados: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el listado de empleados.\n{e}")

    # =========================================================
    # EVENTOS
    # =========================================================
    def _on_nuevo(self) -> None:
        self._clear_form()
        self.entry_cedula.focus_set()

    def _on_guardar(self) -> None:
        try:
            id_rol = self._get_selected_id(self.combo_rol, self.roles_map, "rol")
            id_licencia = self._get_selected_licencia_id()

            nuevo_id = self.service.crear_empleado(
                cedula=self.entry_cedula.get(),
                nombre=self.entry_nombre.get(),
                apellido1=self.entry_apellido1.get(),
                apellido2=self.entry_apellido2.get(),
                telefono=self.entry_telefono.get(),
                correo=self.entry_correo.get(),
                fecha_ingreso=self.entry_fecha_ingreso.get(),
                id_rol=id_rol,
                id_licencia=id_licencia,
            )

            self._load_empleados()
            self._clear_form()

            messagebox.showinfo(
                "Éxito",
                f"Empleado guardado correctamente.\nID asignado: {nuevo_id}"
            )

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al guardar empleado: {e}")
            messagebox.showerror("Error", f"No se pudo guardar el empleado.\n{e}")

    def _on_actualizar(self) -> None:
        try:
            if self.selected_empleado_id is None:
                raise ValueError("Debe seleccionar un empleado para actualizar.")

            id_rol = self._get_selected_id(self.combo_rol, self.roles_map, "rol")
            id_licencia = self._get_selected_licencia_id()

            self.service.actualizar_empleado(
                id_empleado=self.selected_empleado_id,
                cedula=self.entry_cedula.get(),
                nombre=self.entry_nombre.get(),
                apellido1=self.entry_apellido1.get(),
                apellido2=self.entry_apellido2.get(),
                telefono=self.entry_telefono.get(),
                correo=self.entry_correo.get(),
                fecha_ingreso=self.entry_fecha_ingreso.get(),
                id_rol=id_rol,
                id_licencia=id_licencia,
            )

            self._load_empleados()
            self._clear_form()

            messagebox.showinfo("Éxito", "Empleado actualizado correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al actualizar empleado: {e}")
            messagebox.showerror("Error", f"No se pudo actualizar el empleado.\n{e}")

    def _on_eliminar(self) -> None:
        try:
            if self.selected_empleado_id is None:
                raise ValueError("Debe seleccionar un empleado para eliminar.")

            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                "¿Desea eliminar el empleado seleccionado?"
            )
            if not confirm:
                return

            self.service.eliminar_empleado(self.selected_empleado_id)
            self._load_empleados()
            self._clear_form()

            messagebox.showinfo("Éxito", "Empleado eliminado correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al eliminar empleado: {e}")
            messagebox.showerror("Error", f"No se pudo eliminar el empleado.\n{e}")

    def _on_tree_select(self, event=None) -> None:
        try:
            selected = self.tree.selection()
            if not selected:
                return

            item = self.tree.item(selected[0])
            values = item.get("values", [])
            if not values:
                return

            id_empleado = int(values[0])
            empleado = self.service.obtener_empleado_por_id(id_empleado)
            if not empleado:
                return

            self.selected_empleado_id = empleado.id_empleado

            self.entry_cedula.delete(0, tk.END)
            self.entry_cedula.insert(0, empleado.cedula)

            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, empleado.nombre)

            self.entry_apellido1.delete(0, tk.END)
            self.entry_apellido1.insert(0, empleado.apellido1)

            self.entry_apellido2.delete(0, tk.END)
            self.entry_apellido2.insert(0, empleado.apellido2)

            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, empleado.telefono)

            self.entry_correo.delete(0, tk.END)
            self.entry_correo.insert(0, empleado.correo)

            self.entry_fecha_ingreso.delete(0, tk.END)
            self.entry_fecha_ingreso.insert(0, str(empleado.fecha_ingreso))

            self._set_combo_by_id(self.combo_rol, self.roles_map, empleado.id_rol)
            self._set_combo_by_id(self.combo_licencia, self.licencias_map, empleado.id_licencia)

        except Exception as e:
            logger.error(f"Error al seleccionar empleado en la tabla: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el empleado seleccionado.\n{e}")

    # =========================================================
    # HELPERS
    # =========================================================
    def _clear_form(self) -> None:
        self.selected_empleado_id = None

        self.entry_cedula.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido1.delete(0, tk.END)
        self.entry_apellido2.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_fecha_ingreso.delete(0, tk.END)

        self.combo_rol.set("")
        self.combo_licencia.set("")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def _get_selected_id(self, combo: ttk.Combobox, mapping: dict[str, int], label: str) -> int:
        selected_text = combo.get().strip()
        if not selected_text:
            raise ValueError(f"Debe seleccionar un {label}.")
        if selected_text not in mapping:
            raise ValueError(f"El {label} seleccionado no es válido.")
        return mapping[selected_text]

    def _get_selected_licencia_id(self) -> int | None:
        selected_text = self.combo_licencia.get().strip()
        if not selected_text:
            return None
        if selected_text not in self.licencias_map:
            raise ValueError("La licencia seleccionada no es válida.")
        return self.licencias_map[selected_text]

    def _set_combo_by_id(self, combo: ttk.Combobox, mapping: dict[str, int], target_id: int | None) -> None:
        if target_id is None:
            combo.set("")
            return

        for text, value_id in mapping.items():
            if value_id == target_id:
                combo.set(text)
                return

        combo.set("")