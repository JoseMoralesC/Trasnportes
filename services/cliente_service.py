from repositories.cliente_repository import ClienteRepository
from core.logger import get_logger


logger = get_logger("ClienteService")


class ClienteService:
    """
    Lógica de negocio del módulo de clientes.
    """

    def __init__(self) -> None:
        self.repository = ClienteRepository()

    # =========================================================
    # CONSULTAS
    # =========================================================
    def listar_clientes(self):
        return self.repository.listar_clientes()

    def obtener_cliente_por_id(self, id_cliente: int):
        if id_cliente <= 0:
            raise ValueError("El id del cliente es inválido.")
        return self.repository.obtener_cliente_por_id(id_cliente)

    def listar_profesiones(self):
        return self.repository.listar_profesiones()

    def listar_empresas(self):
        return self.repository.listar_empresas()

    def listar_rangos_salariales(self):
        return self.repository.listar_rangos_salariales()

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
        direccion: str,
        id_profesion: int,
        id_empresa: int,
        id_rango_salarial: int,
    ) -> None:
        cedula = cedula.strip()
        nombre = nombre.strip()
        apellido1 = apellido1.strip()
        apellido2 = apellido2.strip()
        telefono = telefono.strip()
        correo = correo.strip()
        direccion = direccion.strip()

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

        if not direccion:
            raise ValueError("La dirección es obligatoria.")

        if id_profesion <= 0:
            raise ValueError("Debe seleccionar una profesión válida.")

        if id_empresa <= 0:
            raise ValueError("Debe seleccionar una empresa válida.")

        if id_rango_salarial <= 0:
            raise ValueError("Debe seleccionar un rango salarial válido.")

    # =========================================================
    # OPERACIONES
    # =========================================================
    def crear_cliente(
        self,
        cedula: str,
        nombre: str,
        apellido1: str,
        apellido2: str,
        id_profesion: int,
        id_empresa: int,
        id_rango_salarial: int,
        telefono: str,
        correo: str,
        direccion: str,
    ) -> int:
        self.validar_datos(
            cedula=cedula,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
            id_profesion=id_profesion,
            id_empresa=id_empresa,
            id_rango_salarial=id_rango_salarial,
        )

        cedula = cedula.strip()
        nombre = nombre.strip()
        apellido1 = apellido1.strip()
        apellido2 = apellido2.strip()
        telefono = telefono.strip()
        correo = correo.strip().lower()
        direccion = direccion.strip()

        if self.repository.existe_cedula(cedula):
            raise ValueError("Ya existe un cliente registrado con esa cédula.")

        if self.repository.existe_correo(correo):
            raise ValueError("Ya existe un cliente registrado con ese correo.")

        nuevo_id = self.repository.obtener_siguiente_id()

        self.repository.insertar_cliente(
            id_cliente=nuevo_id,
            cedula=cedula,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            id_profesion=id_profesion,
            id_empresa=id_empresa,
            id_rango_salarial=id_rango_salarial,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
        )

        logger.info(f"Cliente creado correctamente. ID={nuevo_id}, Cédula={cedula}")
        return nuevo_id

    def actualizar_cliente(
        self,
        id_cliente: int,
        cedula: str,
        nombre: str,
        apellido1: str,
        apellido2: str,
        id_profesion: int,
        id_empresa: int,
        id_rango_salarial: int,
        telefono: str,
        correo: str,
        direccion: str,
    ) -> None:
        if id_cliente <= 0:
            raise ValueError("El id del cliente es inválido.")

        self.validar_datos(
            cedula=cedula,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
            id_profesion=id_profesion,
            id_empresa=id_empresa,
            id_rango_salarial=id_rango_salarial,
        )

        cliente_actual = self.repository.obtener_cliente_por_id(id_cliente)
        if not cliente_actual:
            raise ValueError("El cliente que intenta actualizar no existe.")

        cedula = cedula.strip()
        nombre = nombre.strip()
        apellido1 = apellido1.strip()
        apellido2 = apellido2.strip()
        telefono = telefono.strip()
        correo = correo.strip().lower()
        direccion = direccion.strip()

        # Validación de duplicados excluyendo el propio registro
        if cedula != cliente_actual.cedula and self.repository.existe_cedula(cedula):
            raise ValueError("Ya existe otro cliente registrado con esa cédula.")

        if correo != cliente_actual.correo and self.repository.existe_correo(correo):
            raise ValueError("Ya existe otro cliente registrado con ese correo.")

        self.repository.actualizar_cliente(
            id_cliente=id_cliente,
            cedula=cedula,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            id_profesion=id_profesion,
            id_empresa=id_empresa,
            id_rango_salarial=id_rango_salarial,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
        )

        logger.info(f"Cliente actualizado correctamente. ID={id_cliente}")

    def eliminar_cliente(self, id_cliente: int) -> None:
        existe = self.repository.db.execute(
            "SELECT 1 FROM RESERVACIONES WHERE id_cliente = ?",
            (id_cliente,),
            fecht_one=True
        )
        if existe:
            raise ValueError("No se puede eliminar el cliente porque tiene reservaciones asociadas.")
        
        if id_cliente <= 0:
            raise ValueError("El id del cliente es inválido.")

        cliente_actual = self.repository.obtener_cliente_por_id(id_cliente)
        if not cliente_actual:
            raise ValueError("El cliente que intenta eliminar no existe.")

        self.repository.eliminar_cliente(id_cliente)
        logger.info(f"Cliente eliminado correctamente. ID={id_cliente}")