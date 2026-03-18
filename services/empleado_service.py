from datetime import datetime

from core.logger import get_logger
from repositories.empleado_repository import EmpleadoRepository


logger = get_logger("EmpleadoService")


class EmpleadoService:
    """
    Lógica de negocio del módulo de empleados.
    """

    def __init__(self) -> None:
        self.repository = EmpleadoRepository()

    # =========================================================
    # CONSULTAS
    # =========================================================
    def listar_empleados(self):
        return self.repository.listar_empleados()

    def obtener_empleado_por_id(self, id_empleado: int):
        if id_empleado <= 0:
            raise ValueError("El id del empleado es inválido.")
        return self.repository.obtener_empleado_por_id(id_empleado)

    def listar_roles(self):
        return self.repository.listar_roles()

    def listar_licencias(self):
        return self.repository.listar_licencias()

    def obtener_siguiente_id(self) -> int:
        return self.repository.obtener_siguiente_id()

    # =========================================================
    # VALIDACIONES
    # =========================================================
    def validar_datos(
        self,
        cedula: str,
        nombre: str,
        apellido1: str,
        apellido2: str,
        telefono: str,
        correo: str,
        fecha_ingreso: str,
        id_rol: int,
        id_licencia: int | None,
    ) -> None:
        cedula = cedula.strip()
        nombre = nombre.strip()
        apellido1 = apellido1.strip()
        apellido2 = apellido2.strip()
        telefono = telefono.strip()
        correo = correo.strip()
        fecha_ingreso = fecha_ingreso.strip()

        if not cedula:
            raise ValueError("La cédula es obligatoria.")

        if not nombre:
            raise ValueError("El nombre es obligatorio.")

        if not apellido1:
            raise ValueError("El primer apellido es obligatorio.")

        if not apellido2:
            raise ValueError("El segundo apellido es obligatorio.")

        if not telefono:
            raise ValueError("El teléfono es obligatorio.")

        if not correo:
            raise ValueError("El correo es obligatorio.")

        if "@" not in correo or "." not in correo:
            raise ValueError("El correo no tiene un formato válido.")

        if not fecha_ingreso:
            raise ValueError("La fecha de ingreso es obligatoria.")

        try:
            datetime.strptime(fecha_ingreso, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha de ingreso debe tener formato YYYY-MM-DD.")

        if id_rol <= 0:
            raise ValueError("Debe seleccionar un rol válido.")

        if id_licencia is not None and id_licencia <= 0:
            raise ValueError("La licencia seleccionada no es válida.")

    # =========================================================
    # OPERACIONES
    # =========================================================
    def crear_empleado(
        self,
        cedula: str,
        nombre: str,
        apellido1: str,
        apellido2: str,
        telefono: str,
        correo: str,
        fecha_ingreso: str,
        id_rol: int,
        id_licencia: int | None,
    ) -> int:
        self.validar_datos(
            cedula=cedula,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            telefono=telefono,
            correo=correo,
            fecha_ingreso=fecha_ingreso,
            id_rol=id_rol,
            id_licencia=id_licencia,
        )

        cedula = cedula.strip()
        nombre = nombre.strip()
        apellido1 = apellido1.strip()
        apellido2 = apellido2.strip()
        telefono = telefono.strip()
        correo = correo.strip().lower()
        fecha_ingreso = fecha_ingreso.strip()

        if self.repository.existe_cedula(cedula):
            raise ValueError("Ya existe un empleado registrado con esa cédula.")

        if self.repository.existe_correo(correo):
            raise ValueError("Ya existe un empleado registrado con ese correo.")

        nuevo_id = self.repository.obtener_siguiente_id()

        self.repository.insertar_empleado(
            id_empleado=nuevo_id,
            cedula=cedula,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            telefono=telefono,
            correo=correo,
            fecha_ingreso=fecha_ingreso,
            id_rol=id_rol,
            id_licencia=id_licencia,
        )

        logger.info(f"Empleado creado correctamente. ID={nuevo_id}, Cédula={cedula}")
        return nuevo_id

    def actualizar_empleado(
        self,
        id_empleado: int,
        cedula: str,
        nombre: str,
        apellido1: str,
        apellido2: str,
        telefono: str,
        correo: str,
        fecha_ingreso: str,
        id_rol: int,
        id_licencia: int | None,
    ) -> None:
        if id_empleado <= 0:
            raise ValueError("El id del empleado es inválido.")

        self.validar_datos(
            cedula=cedula,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            telefono=telefono,
            correo=correo,
            fecha_ingreso=fecha_ingreso,
            id_rol=id_rol,
            id_licencia=id_licencia,
        )

        empleado_actual = self.repository.obtener_empleado_por_id(id_empleado)
        if not empleado_actual:
            raise ValueError("El empleado que intenta actualizar no existe.")

        cedula = cedula.strip()
        nombre = nombre.strip()
        apellido1 = apellido1.strip()
        apellido2 = apellido2.strip()
        telefono = telefono.strip()
        correo = correo.strip().lower()
        fecha_ingreso = fecha_ingreso.strip()

        if cedula != empleado_actual.cedula and self.repository.existe_cedula(cedula):
            raise ValueError("Ya existe otro empleado registrado con esa cédula.")

        if correo != empleado_actual.correo and self.repository.existe_correo(correo):
            raise ValueError("Ya existe otro empleado registrado con ese correo.")

        self.repository.actualizar_empleado(
            id_empleado=id_empleado,
            cedula=cedula,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            telefono=telefono,
            correo=correo,
            fecha_ingreso=fecha_ingreso,
            id_rol=id_rol,
            id_licencia=id_licencia,
        )

        logger.info(f"Empleado actualizado correctamente. ID={id_empleado}")

    def eliminar_empleado(self, id_empleado: int) -> None:
        if id_empleado <= 0:
            raise ValueError("El id del empleado es inválido.")

        empleado_actual = self.repository.obtener_empleado_por_id(id_empleado)
        if not empleado_actual:
            raise ValueError("El empleado que intenta eliminar no existe.")

        self.repository.eliminar_empleado(id_empleado)
        logger.info(f"Empleado eliminado correctamente. ID={id_empleado}")