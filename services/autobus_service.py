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

    def obtener_dekra_actual_por_autobus(self, id_autobus: int):
        if id_autobus <= 0:
            raise ValueError("El id del autobús es inválido.")
        return self.repository.obtener_dekra_actual_por_autobus(id_autobus)

    def obtener_marchamo_actual_por_autobus(self, id_autobus: int):
        if id_autobus <= 0:
            raise ValueError("El id del autobús es inválido.")
        return self.repository.obtener_marchamo_actual_por_autobus(id_autobus)

    def listar_marcas(self):
        return self.repository.listar_marcas()

    def listar_modelos(self):
        return self.repository.listar_modelos()

    def listar_estados(self):
        return self.repository.listar_estados()

    def listar_tipos_autobus(self):
        return self.repository.listar_tipos_autobus()

    def listar_estados_dekra(self):
        return self.repository.listar_estados_dekra()

    def listar_estados_marchamo(self):
        return self.repository.listar_estados_marchamo()

    def obtener_siguiente_id(self) -> int:
        return self.repository.obtener_siguiente_id()

    def obtener_siguiente_numero_unidad(self) -> tuple[int, str]:
        siguiente_id = self.repository.obtener_siguiente_id_num_unidad()
        unidad = f"U-{siguiente_id:03d}"
        return siguiente_id, unidad

    # =========================================================
    # HELPERS
    # =========================================================
    def _normalizar_texto(self, valor: str) -> str:
        return valor.strip()

    def _normalizar_mayuscula(self, valor: str) -> str:
        return valor.strip().upper()

    def _parsear_fecha(self, valor: str, nombre_campo: str):
        try:
            return datetime.strptime(valor.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"La {nombre_campo} no tiene un formato válido (YYYY-MM-DD).")

    # =========================================================
    # VALIDACIONES AUTOBÚS
    # =========================================================
    def validar_datos(
        self,
        placa: str,
        id_marca: int,
        id_modelo: int,
        anio: int,
        capacidad: int,
        id_estado: int,
        id_tipo_autobus: int,
    ) -> None:
        placa = self._normalizar_mayuscula(placa)

        if not placa:
            raise ValueError("La placa es obligatoria.")

        if len(placa) < 5:
            raise ValueError("La placa no tiene un formato válido.")

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
    # VALIDACIONES DEKRA
    # =========================================================
    def validar_datos_dekra(
        self,
        numero_dekra: str,
        fecha_emision: str,
        fecha_vencimiento: str,
        id_estado_dekra: int,
    ) -> tuple[str, str, str]:
        numero_dekra = self._normalizar_mayuscula(numero_dekra)

        if not numero_dekra:
            raise ValueError("El número de DEKRA es obligatorio.")

        if len(numero_dekra) < 4:
            raise ValueError("El número de DEKRA no tiene un formato válido.")

        if id_estado_dekra <= 0:
            raise ValueError("Debe seleccionar un estado de DEKRA válido.")

        fecha_emision_date = self._parsear_fecha(fecha_emision, "fecha de emisión del DEKRA")
        fecha_vencimiento_date = self._parsear_fecha(
            fecha_vencimiento,
            "fecha de vencimiento del DEKRA",
        )

        if fecha_vencimiento_date <= fecha_emision_date:
            raise ValueError("La fecha de vencimiento del DEKRA debe ser mayor a la fecha de emisión.")

        return (
            numero_dekra,
            fecha_emision_date.isoformat(),
            fecha_vencimiento_date.isoformat(),
        )

    # =========================================================
    # VALIDACIONES MARCHAMO
    # =========================================================
    def validar_datos_marchamo(
        self,
        numero_marchamo: str,
        periodo: str,
        fecha_pago: str,
        fecha_vencimiento: str,
        id_estado_marchamo: int,
    ) -> tuple[str, str, str, str]:
        numero_marchamo = self._normalizar_mayuscula(numero_marchamo)
        periodo = self._normalizar_texto(periodo)

        if not numero_marchamo:
            raise ValueError("El número de marchamo es obligatorio.")

        if len(numero_marchamo) < 4:
            raise ValueError("El número de marchamo no tiene un formato válido.")

        if not periodo:
            raise ValueError("El período del marchamo es obligatorio.")

        if not periodo.isdigit() or len(periodo) != 4:
            raise ValueError("El período del marchamo debe tener formato de año, por ejemplo: 2026.")

        if id_estado_marchamo <= 0:
            raise ValueError("Debe seleccionar un estado de marchamo válido.")

        fecha_pago_date = self._parsear_fecha(fecha_pago, "fecha de pago del marchamo")
        fecha_vencimiento_date = self._parsear_fecha(
            fecha_vencimiento,
            "fecha de vencimiento del marchamo",
        )

        if fecha_vencimiento_date <= fecha_pago_date:
            raise ValueError("La fecha de vencimiento del marchamo debe ser mayor a la fecha de pago.")

        return (
            numero_marchamo,
            periodo,
            fecha_pago_date.isoformat(),
            fecha_vencimiento_date.isoformat(),
        )

    # =========================================================
    # OPERACIONES
    # =========================================================
    def crear_autobus(
        self,
        placa: str,
        id_marca: int,
        id_modelo: int,
        anio: int,
        capacidad: int,
        id_estado: int,
        id_tipo_autobus: int,
        numero_dekra: str,
        fecha_emision_dekra: str,
        fecha_vencimiento_dekra: str,
        id_estado_dekra: int,
        numero_marchamo: str,
        periodo_marchamo: str,
        fecha_pago_marchamo: str,
        fecha_vencimiento_marchamo: str,
        id_estado_marchamo: int,
    ) -> int:
        self.validar_datos(
            placa=placa,
            id_marca=id_marca,
            id_modelo=id_modelo,
            anio=anio,
            capacidad=capacidad,
            id_estado=id_estado,
            id_tipo_autobus=id_tipo_autobus,
        )

        numero_dekra, fecha_emision_dekra, fecha_vencimiento_dekra = self.validar_datos_dekra(
            numero_dekra=numero_dekra,
            fecha_emision=fecha_emision_dekra,
            fecha_vencimiento=fecha_vencimiento_dekra,
            id_estado_dekra=id_estado_dekra,
        )

        (
            numero_marchamo,
            periodo_marchamo,
            fecha_pago_marchamo,
            fecha_vencimiento_marchamo,
        ) = self.validar_datos_marchamo(
            numero_marchamo=numero_marchamo,
            periodo=periodo_marchamo,
            fecha_pago=fecha_pago_marchamo,
            fecha_vencimiento=fecha_vencimiento_marchamo,
            id_estado_marchamo=id_estado_marchamo,
        )

        placa = self._normalizar_mayuscula(placa)

        if self.repository.existe_placa(placa):
            raise ValueError("Ya existe un autobús registrado con esa placa.")

        if self.repository.existe_numero_dekra(numero_dekra):
            raise ValueError("Ya existe un registro de DEKRA con ese número.")

        if self.repository.existe_numero_marchamo(numero_marchamo):
            raise ValueError("Ya existe un registro de marchamo con ese número.")

        nuevo_id_autobus = self.repository.obtener_siguiente_id()
        nuevo_id_num_unidad, nueva_unidad = self.obtener_siguiente_numero_unidad()

        if self.repository.existe_marchamo_por_periodo_autobus(
            id_autobus=nuevo_id_autobus,
            periodo=periodo_marchamo,
        ):
            raise ValueError("Ya existe un marchamo registrado para ese autobús en ese período.")

        self.repository.insertar_numero_unidad(
            id_num_unidad=nuevo_id_num_unidad,
            unidad=nueva_unidad,
        )

        self.repository.insertar_autobus(
            id_autobus=nuevo_id_autobus,
            placa=placa,
            id_num_unidad=nuevo_id_num_unidad,
            id_marca=id_marca,
            id_modelo=id_modelo,
            anio=anio,
            capacidad=capacidad,
            id_estado=id_estado,
            id_tipo_autobus=id_tipo_autobus,
        )

        nuevo_id_dekra = self.repository.obtener_siguiente_id_dekra()
        self.repository.insertar_dekra(
            id_dekra=nuevo_id_dekra,
            id_autobus=nuevo_id_autobus,
            numero_dekra=numero_dekra,
            fecha_emision=fecha_emision_dekra,
            fecha_vencimiento=fecha_vencimiento_dekra,
            id_estado=id_estado_dekra,
        )

        nuevo_id_marchamo = self.repository.obtener_siguiente_id_marchamo()
        self.repository.insertar_marchamo(
            id_marchamo=nuevo_id_marchamo,
            id_autobus=nuevo_id_autobus,
            numero_marchamo=numero_marchamo,
            periodo=periodo_marchamo,
            fecha_pago=fecha_pago_marchamo,
            fecha_vencimiento=fecha_vencimiento_marchamo,
            id_estado=id_estado_marchamo,
        )

        logger.info(
            f"Autobús creado correctamente. ID={nuevo_id_autobus}, "
            f"Unidad={nueva_unidad}, Placa={placa}, "
            f"DEKRA={numero_dekra}, MARCHAMO={numero_marchamo}"
        )
        return nuevo_id_autobus

    def actualizar_autobus(
        self,
        id_autobus: int,
        placa: str,
        id_marca: int,
        id_modelo: int,
        anio: int,
        capacidad: int,
        id_estado: int,
        id_tipo_autobus: int,
        numero_dekra: str,
        fecha_emision_dekra: str,
        fecha_vencimiento_dekra: str,
        id_estado_dekra: int,
        numero_marchamo: str,
        periodo_marchamo: str,
        fecha_pago_marchamo: str,
        fecha_vencimiento_marchamo: str,
        id_estado_marchamo: int,
    ) -> None:
        if id_autobus <= 0:
            raise ValueError("El id del autobús es inválido.")

        self.validar_datos(
            placa=placa,
            id_marca=id_marca,
            id_modelo=id_modelo,
            anio=anio,
            capacidad=capacidad,
            id_estado=id_estado,
            id_tipo_autobus=id_tipo_autobus,
        )

        numero_dekra, fecha_emision_dekra, fecha_vencimiento_dekra = self.validar_datos_dekra(
            numero_dekra=numero_dekra,
            fecha_emision=fecha_emision_dekra,
            fecha_vencimiento=fecha_vencimiento_dekra,
            id_estado_dekra=id_estado_dekra,
        )

        (
            numero_marchamo,
            periodo_marchamo,
            fecha_pago_marchamo,
            fecha_vencimiento_marchamo,
        ) = self.validar_datos_marchamo(
            numero_marchamo=numero_marchamo,
            periodo=periodo_marchamo,
            fecha_pago=fecha_pago_marchamo,
            fecha_vencimiento=fecha_vencimiento_marchamo,
            id_estado_marchamo=id_estado_marchamo,
        )

        autobus_actual = self.repository.obtener_autobus_por_id(id_autobus)
        if not autobus_actual:
            raise ValueError("El autobús que intenta actualizar no existe.")

        dekra_actual = self.repository.obtener_dekra_actual_por_autobus(id_autobus)
        marchamo_actual = self.repository.obtener_marchamo_actual_por_autobus(id_autobus)

        placa = self._normalizar_mayuscula(placa)

        if placa != autobus_actual.placa and self.repository.existe_placa(placa):
            raise ValueError("Ya existe otro autobús registrado con esa placa.")

        excluir_id_dekra = dekra_actual.id_dekra if dekra_actual else None
        if self.repository.existe_numero_dekra(numero_dekra, excluir_id_dekra=excluir_id_dekra):
            raise ValueError("Ya existe otro registro de DEKRA con ese número.")

        excluir_id_marchamo = marchamo_actual.id_marchamo if marchamo_actual else None
        if self.repository.existe_numero_marchamo(
            numero_marchamo,
            excluir_id_marchamo=excluir_id_marchamo,
        ):
            raise ValueError("Ya existe otro registro de marchamo con ese número.")

        if self.repository.existe_marchamo_por_periodo_autobus(
            id_autobus=id_autobus,
            periodo=periodo_marchamo,
            excluir_id_marchamo=excluir_id_marchamo,
        ):
            raise ValueError("Ya existe otro marchamo registrado para ese autobús en ese período.")

        self.repository.actualizar_autobus(
            id_autobus=id_autobus,
            placa=placa,
            id_num_unidad=autobus_actual.id_num_unidad,
            id_marca=id_marca,
            id_modelo=id_modelo,
            anio=anio,
            capacidad=capacidad,
            id_estado=id_estado,
            id_tipo_autobus=id_tipo_autobus,
        )

        if dekra_actual:
            self.repository.actualizar_dekra(
                id_dekra=dekra_actual.id_dekra,
                numero_dekra=numero_dekra,
                fecha_emision=fecha_emision_dekra,
                fecha_vencimiento=fecha_vencimiento_dekra,
                id_estado=id_estado_dekra,
            )
        else:
            nuevo_id_dekra = self.repository.obtener_siguiente_id_dekra()
            self.repository.insertar_dekra(
                id_dekra=nuevo_id_dekra,
                id_autobus=id_autobus,
                numero_dekra=numero_dekra,
                fecha_emision=fecha_emision_dekra,
                fecha_vencimiento=fecha_vencimiento_dekra,
                id_estado=id_estado_dekra,
            )

        if marchamo_actual:
            self.repository.actualizar_marchamo(
                id_marchamo=marchamo_actual.id_marchamo,
                numero_marchamo=numero_marchamo,
                periodo=periodo_marchamo,
                fecha_pago=fecha_pago_marchamo,
                fecha_vencimiento=fecha_vencimiento_marchamo,
                id_estado=id_estado_marchamo,
            )
        else:
            nuevo_id_marchamo = self.repository.obtener_siguiente_id_marchamo()
            self.repository.insertar_marchamo(
                id_marchamo=nuevo_id_marchamo,
                id_autobus=id_autobus,
                numero_marchamo=numero_marchamo,
                periodo=periodo_marchamo,
                fecha_pago=fecha_pago_marchamo,
                fecha_vencimiento=fecha_vencimiento_marchamo,
                id_estado=id_estado_marchamo,
            )

        logger.info(
            f"Autobús actualizado correctamente. ID={id_autobus}, "
            f"DEKRA={numero_dekra}, MARCHAMO={numero_marchamo}"
        )

    def eliminar_autobus(self, id_autobus: int) -> None:
        if id_autobus <= 0:
            raise ValueError("El id del autobús es inválido.")

        autobus_actual = self.repository.obtener_autobus_por_id(id_autobus)
        if not autobus_actual:
            raise ValueError("El autobús que intenta eliminar no existe.")

        self.repository.eliminar_autobus(id_autobus)
        logger.info(f"Autobús eliminado correctamente. ID={id_autobus}")