from datetime import datetime

from core.logger import get_logger
from repositories.autobus_repository import AutobusRepository


logger = get_logger("AutobusService")


class AutobusService:
    """
    Lógica de negocio del módulo de autobuses.
    """

    def __init__(self) -> None:
        self.repository = AutobusRepository()

    # =========================================================
    # CONSULTAS
    # =========================================================
    def listar_autobuses(self):
        return self.repository.listar_autobuses()

    def obtener_autobus_por_id(self, id_autobus: int):
        if id_autobus <= 0:
            raise ValueError("El id del autobús es inválido.")
        return self.repository.obtener_autobus_por_id(id_autobus)

    def listar_numeros_unidad(self):
        return self.repository.listar_numeros_unidad()

    def listar_marcas(self):
        return self.repository.listar_marcas()

    def listar_modelos(self):
        return self.repository.listar_modelos()

    def listar_estados(self):
        return self.repository.listar_estados()

    def listar_tipos_autobus(self):
        return self.repository.listar_tipos_autobus()

    def obtener_siguiente_id(self) -> int:
        return self.repository.obtener_siguiente_id()

    # =========================================================
    # VALIDACIONES
    # =========================================================
    def validar_datos(
        self,
        placa: str,
        id_num_unidad: int,
        id_marca: int,
        id_modelo: int,
        anio: int,
        capacidad: int,
        id_estado: int,
        id_tipo_autobus: int,
    ) -> None:
        placa = placa.strip().upper()

        if not placa:
            raise ValueError("La placa es obligatoria.")

        if len(placa) < 5:
            raise ValueError("La placa no tiene un formato válido.")

        if id_num_unidad <= 0:
            raise ValueError("Debe seleccionar un número de unidad válido.")

        if id_marca <= 0:
            raise ValueError("Debe seleccionar una marca válida.")

        if id_modelo <= 0:
            raise ValueError("Debe seleccionar un modelo válido.")

        if id_estado <= 0:
            raise ValueError("Debe seleccionar un estado válido.")

        if id_tipo_autobus <= 0:
            raise ValueError("Debe seleccionar un tipo de autobús válido.")

        if anio <= 0:
            raise ValueError("El año es obligatorio.")

        current_year = datetime.now().year
        if anio < 1950 or anio > current_year + 1:
            raise ValueError("El año del autobús no es válido.")

        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        if capacidad > 100:
            raise ValueError("La capacidad del autobús no es válida.")

    # =========================================================
    # OPERACIONES
    # =========================================================
    def crear_autobus(
        self,
        placa: str,
        id_num_unidad: int,
        id_marca: int,
        id_modelo: int,
        anio: int,
        capacidad: int,
        id_estado: int,
        id_tipo_autobus: int,
    ) -> int:
        self.validar_datos(
            placa=placa,
            id_num_unidad=id_num_unidad,
            id_marca=id_marca,
            id_modelo=id_modelo,
            anio=anio,
            capacidad=capacidad,
            id_estado=id_estado,
            id_tipo_autobus=id_tipo_autobus,
        )

        placa = placa.strip().upper()

        if self.repository.existe_placa(placa):
            raise ValueError("Ya existe un autobús registrado con esa placa.")

        nuevo_id = self.repository.obtener_siguiente_id()

        self.repository.insertar_autobus(
            id_autobus=nuevo_id,
            placa=placa,
            id_num_unidad=id_num_unidad,
            id_marca=id_marca,
            id_modelo=id_modelo,
            anio=anio,
            capacidad=capacidad,
            id_estado=id_estado,
            id_tipo_autobus=id_tipo_autobus,
        )

        logger.info(f"Autobús creado correctamente. ID={nuevo_id}, Placa={placa}")
        return nuevo_id

    def actualizar_autobus(
        self,
        id_autobus: int,
        placa: str,
        id_num_unidad: int,
        id_marca: int,
        id_modelo: int,
        anio: int,
        capacidad: int,
        id_estado: int,
        id_tipo_autobus: int,
    ) -> None:
        if id_autobus <= 0:
            raise ValueError("El id del autobús es inválido.")

        self.validar_datos(
            placa=placa,
            id_num_unidad=id_num_unidad,
            id_marca=id_marca,
            id_modelo=id_modelo,
            anio=anio,
            capacidad=capacidad,
            id_estado=id_estado,
            id_tipo_autobus=id_tipo_autobus,
        )

        autobus_actual = self.repository.obtener_autobus_por_id(id_autobus)
        if not autobus_actual:
            raise ValueError("El autobús que intenta actualizar no existe.")

        placa = placa.strip().upper()

        if placa != autobus_actual.placa and self.repository.existe_placa(placa):
            raise ValueError("Ya existe otro autobús registrado con esa placa.")

        self.repository.actualizar_autobus(
            id_autobus=id_autobus,
            placa=placa,
            id_num_unidad=id_num_unidad,
            id_marca=id_marca,
            id_modelo=id_modelo,
            anio=anio,
            capacidad=capacidad,
            id_estado=id_estado,
            id_tipo_autobus=id_tipo_autobus,
        )

        logger.info(f"Autobús actualizado correctamente. ID={id_autobus}")

    def eliminar_autobus(self, id_autobus: int) -> None:
        if id_autobus <= 0:
            raise ValueError("El id del autobús es inválido.")

        autobus_actual = self.repository.obtener_autobus_por_id(id_autobus)
        if not autobus_actual:
            raise ValueError("El autobús que intenta eliminar no existe.")

        self.repository.eliminar_autobus(id_autobus)
        logger.info(f"Autobús eliminado correctamente. ID={id_autobus}")