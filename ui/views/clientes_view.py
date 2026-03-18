import tkinter as tk
from tkinter import ttk, messagebox

from core.logger import get_logger
from services.cliente_service import ClienteService


logger = get_logger("ClientesView")


class ClientesView(ttk.Frame):
    """
    Vista del módulo de clientes.
    Incluye:
    - formulario
    - combos de catálogos
    - tabla de listado
    - acciones CRUD básicas
    """

    def __init__(self, master) -> None:
        super().__init__(master, style="App.TFrame")
        self.service = ClienteService()

        self.selected_cliente_id: int | None = None

        self.profesiones_map: dict[str, int] = {}
        self.empresas_map: dict[str, int] = {}
        self.rangos_map: dict[str, int] = {}

        self._build_ui()
        self._load_catalogs()
        self._load_clientes()

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

        ttk.Label(form_card, text="Gestión de Clientes", style="Title.TLabel").grid(
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
        ttk.Label(form_card, text="Profesión").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=6)
        self.combo_profesion = ttk.Combobox(form_card, state="readonly")
        self.combo_profesion.grid(row=4, column=0, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Empresa").grid(row=3, column=1, sticky="w", padx=8, pady=6)
        self.combo_empresa = ttk.Combobox(form_card, state="readonly")
        self.combo_empresa.grid(row=4, column=1, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Rango salarial").grid(row=3, column=2, sticky="w", padx=8, pady=6)
        self.combo_rango = ttk.Combobox(form_card, state="readonly")
        self.combo_rango.grid(row=4, column=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(form_card, text="Teléfono").grid(row=3, column=3, sticky="w", padx=(8, 0), pady=6)
        self.entry_telefono = ttk.Entry(form_card)
        self.entry_telefono.grid(row=4, column=3, sticky="ew", padx=(8, 0), pady=(0, 8))

        # Fila 3
        ttk.Label(form_card, text="Correo").grid(row=5, column=0, sticky="w", padx=(0, 8), pady=6)
        self.entry_correo = ttk.Entry(form_card)
        self.entry_correo.grid(row=6, column=0, columnspan=2, sticky="ew", padx=(0, 8), pady=(0, 8))

        ttk.Label(form_card, text="Dirección").grid(row=5, column=2, sticky="w", padx=8, pady=6)
        self.entry_direccion = ttk.Entry(form_card)
        self.entry_direccion.grid(row=6, column=2, columnspan=2, sticky="ew", padx=(8, 0), pady=(0, 8))

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

        ttk.Label(table_card, text="Listado de Clientes", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        columns = (
            "id_cliente",
            "cedula",
            "nombre_completo",
            "profesion",
            "empresa",
            "rango",
            "telefono",
            "correo",
            "direccion",
        )

        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=14)
        self.tree.grid(row=1, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.heading("id_cliente", text="ID")
        self.tree.heading("cedula", text="Cédula")
        self.tree.heading("nombre_completo", text="Nombre completo")
        self.tree.heading("profesion", text="Profesión")
        self.tree.heading("empresa", text="Empresa")
        self.tree.heading("rango", text="Rango salarial")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("direccion", text="Dirección")

        self.tree.column("id_cliente", width=70, anchor="center")
        self.tree.column("cedula", width=110, anchor="center")
        self.tree.column("nombre_completo", width=210)
        self.tree.column("profesion", width=120)
        self.tree.column("empresa", width=150)
        self.tree.column("rango", width=120, anchor="center")
        self.tree.column("telefono", width=100, anchor="center")
        self.tree.column("correo", width=180)
        self.tree.column("direccion", width=180)

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    # =========================================================
    # CARGAS INICIALES
    # =========================================================
    def _load_catalogs(self) -> None:
        try:
            profesiones = self.service.listar_profesiones()
            empresas = self.service.listar_empresas()
            rangos = self.service.listar_rangos_salariales()

            self.profesiones_map = {
                row.nombre_profesion: row.id_profesion for row in profesiones
            }
            self.empresas_map = {
                row.nombre_empresa: row.id_empresa for row in empresas
            }
            self.rangos_map = {
                row.descripcion_rango: row.id_rango_salarial for row in rangos
            }

            self.combo_profesion["values"] = list(self.profesiones_map.keys())
            self.combo_empresa["values"] = list(self.empresas_map.keys())
            self.combo_rango["values"] = list(self.rangos_map.keys())

        except Exception as e:
            logger.error(f"Error al cargar catálogos de clientes: {e}")
            messagebox.showerror("Error", f"No se pudieron cargar los catálogos.\n{e}")

    def _load_clientes(self) -> None:
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            clientes = self.service.listar_clientes()

            for row in clientes:
                nombre_completo = f"{row.nombre} {row.apellido1} {row.apellido2}"
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row.id_cliente,
                        row.cedula,
                        nombre_completo,
                        row.nombre_profesion,
                        row.nombre_empresa,
                        row.descripcion_rango,
                        row.telefono,
                        row.correo,
                        row.direccion,
                    ),
                )

        except Exception as e:
            logger.error(f"Error al cargar clientes: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el listado de clientes.\n{e}")

    # =========================================================
    # EVENTOS
    # =========================================================
    def _on_nuevo(self) -> None:
        self._clear_form()
        self.entry_cedula.focus_set()

    def _on_guardar(self) -> None:
        try:
            id_profesion = self._get_selected_id(self.combo_profesion, self.profesiones_map, "profesión")
            id_empresa = self._get_selected_id(self.combo_empresa, self.empresas_map, "empresa")
            id_rango = self._get_selected_id(self.combo_rango, self.rangos_map, "rango salarial")

            nuevo_id = self.service.crear_cliente(
                cedula=self.entry_cedula.get(),
                nombre=self.entry_nombre.get(),
                apellido1=self.entry_apellido1.get(),
                apellido2=self.entry_apellido2.get(),
                id_profesion=id_profesion,
                id_empresa=id_empresa,
                id_rango_salarial=id_rango,
                telefono=self.entry_telefono.get(),
                correo=self.entry_correo.get(),
                direccion=self.entry_direccion.get(),
            )

            self._load_clientes()
            self._clear_form()

            messagebox.showinfo(
                "Éxito",
                f"Cliente guardado correctamente.\nID asignado: {nuevo_id}"
            )

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al guardar cliente: {e}")
            messagebox.showerror("Error", f"No se pudo guardar el cliente.\n{e}")

    def _on_actualizar(self) -> None:
        try:
            if self.selected_cliente_id is None:
                raise ValueError("Debe seleccionar un cliente para actualizar.")

            id_profesion = self._get_selected_id(self.combo_profesion, self.profesiones_map, "profesión")
            id_empresa = self._get_selected_id(self.combo_empresa, self.empresas_map, "empresa")
            id_rango = self._get_selected_id(self.combo_rango, self.rangos_map, "rango salarial")

            self.service.actualizar_cliente(
                id_cliente=self.selected_cliente_id,
                cedula=self.entry_cedula.get(),
                nombre=self.entry_nombre.get(),
                apellido1=self.entry_apellido1.get(),
                apellido2=self.entry_apellido2.get(),
                id_profesion=id_profesion,
                id_empresa=id_empresa,
                id_rango_salarial=id_rango,
                telefono=self.entry_telefono.get(),
                correo=self.entry_correo.get(),
                direccion=self.entry_direccion.get(),
            )

            self._load_clientes()
            self._clear_form()

            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al actualizar cliente: {e}")
            messagebox.showerror("Error", f"No se pudo actualizar el cliente.\n{e}")

    def _on_eliminar(self) -> None:
        try:
            if self.selected_cliente_id is None:
                raise ValueError("Debe seleccionar un cliente para eliminar.")

            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                "¿Desea eliminar el cliente seleccionado?"
            )
            if not confirm:
                return

            self.service.eliminar_cliente(self.selected_cliente_id)
            self._load_clientes()
            self._clear_form()

            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")

        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            logger.error(f"Error al eliminar cliente: {e}")
            messagebox.showerror("Error", f"No se pudo eliminar el cliente.\n{e}")

    def _on_tree_select(self, event=None) -> None:
        try:
            selected = self.tree.selection()
            if not selected:
                return

            item = self.tree.item(selected[0])
            values = item.get("values", [])
            if not values:
                return

            id_cliente = int(values[0])
            cliente = self.service.obtener_cliente_por_id(id_cliente)
            if not cliente:
                return

            self.selected_cliente_id = cliente.id_cliente

            self.entry_cedula.delete(0, tk.END)
            self.entry_cedula.insert(0, cliente.cedula)

            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, cliente.nombre)

            self.entry_apellido1.delete(0, tk.END)
            self.entry_apellido1.insert(0, cliente.apellido1)

            self.entry_apellido2.delete(0, tk.END)
            self.entry_apellido2.insert(0, cliente.apellido2)

            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, cliente.telefono)

            self.entry_correo.delete(0, tk.END)
            self.entry_correo.insert(0, cliente.correo)

            self.entry_direccion.delete(0, tk.END)
            self.entry_direccion.insert(0, cliente.direccion)

            self._set_combo_by_id(self.combo_profesion, self.profesiones_map, cliente.id_profesion)
            self._set_combo_by_id(self.combo_empresa, self.empresas_map, cliente.id_empresa)
            self._set_combo_by_id(self.combo_rango, self.rangos_map, cliente.id_rango_salarial)

        except Exception as e:
            logger.error(f"Error al seleccionar cliente en la tabla: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el cliente seleccionado.\n{e}")

    # =========================================================
    # HELPERS
    # =========================================================
    def _clear_form(self) -> None:
        self.selected_cliente_id = None

        self.entry_cedula.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido1.delete(0, tk.END)
        self.entry_apellido2.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)

        self.combo_profesion.set("")
        self.combo_empresa.set("")
        self.combo_rango.set("")

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