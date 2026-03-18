from datetime import datetime

from core.logger import get_logger
from repositories.pago_repository import PagoRepository


logger = get_logger("PagoService")


class PagoService:
    """
    Lógica de negocio del módulo de pagos.
    """

    def __init__(self) -> None:
        self.repository = PagoRepository()

    # =========================================================
    # CONSULTAS
    # =========================================================
    def listar_pagos(self):
        return self.repository.listar_pagos()

    def obtener_pago_por_id(self, id_pago: int):
        if id_pago <= 0:
            raise ValueError("El id del pago es inválido.")
        return self.repository.obtener_pago_por_id(id_pago)

    def listar_facturas(self):
        return self.repository.listar_facturas()

    def listar_metodos_pago(self):
        return self.repository.listar_metodos_pago()

    def listar_estados_pago(self):
        return self.repository.listar_estados_pago()

    def obtener_siguiente_id(self) -> int:
        return self.repository.obtener_siguiente_id()

    # =========================================================
    # VALIDACIONES
    # =========================================================
    def validar_datos(
        self,
        id_factura: int,
        id_metodo_pago: int,
        fecha_pago: str,
        monto_pagado: float,
        referencia_pago: str,
        id_estado: int,
    ) -> None:
        fecha_pago = fecha_pago.strip()
        referencia_pago = referencia_pago.strip()

        if id_factura <= 0:
            raise ValueError("Debe seleccionar una factura válida.")

        if id_metodo_pago <= 0:
            raise ValueError("Debe seleccionar un método de pago válido.")

        if not fecha_pago:
            raise ValueError("La fecha de pago es obligatoria.")

        try:
            datetime.strptime(fecha_pago, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha de pago debe tener formato YYYY-MM-DD.")

        if monto_pagado <= 0:
            raise ValueError("El monto pagado debe ser mayor que cero.")

        if not referencia_pago:
            raise ValueError("La referencia de pago es obligatoria.")

        if id_estado <= 0:
            raise ValueError("Debe seleccionar un estado válido.")

    # =========================================================
    # HELPERS
    # =========================================================
    def obtener_total_factura(self, id_factura: int) -> float:
        if id_factura <= 0:
            raise ValueError("La factura seleccionada no es válida.")

        row = self.repository.obtener_total_factura(id_factura)
        if not row:
            raise ValueError("No se encontró el total de la factura seleccionada.")

        return float(row.total)

    # =========================================================
    # OPERACIONES
    # =========================================================
    def crear_pago(
        self,
        id_factura: int,
        id_metodo_pago: int,
        fecha_pago: str,
        monto_pagado: float,
        referencia_pago: str,
        id_estado: int,
    ) -> int:
        
        total_factura = self.obtener_total_factura(id_factura)

        if monto_pagado > total_factura:
            raise ValueError("El monto pagado no puede ser mayor al total de la factura.")

        self.validar_datos(
            id_factura=id_factura,
            id_metodo_pago=id_metodo_pago,
            fecha_pago=fecha_pago,
            monto_pagado=monto_pagado,
            referencia_pago=referencia_pago,
            id_estado=id_estado,
        )

        referencia_pago = referencia_pago.strip().upper()
        fecha_pago = fecha_pago.strip()

        if self.repository.existe_referencia_pago(referencia_pago):
            raise ValueError("Ya existe un pago registrado con esa referencia.")

        nuevo_id = self.repository.obtener_siguiente_id()

        self.repository.insertar_pago(
            id_pago=nuevo_id,
            id_factura=id_factura,
            id_metodo_pago=id_metodo_pago,
            fecha_pago=fecha_pago,
            monto_pagado=monto_pagado,
            referencia_pago=referencia_pago,
            id_estado=id_estado,
        )

        logger.info(f"Pago creado correctamente. ID={nuevo_id}, Referencia={referencia_pago}")
        return nuevo_id

    def actualizar_pago(
        self,
        id_pago: int,
        id_factura: int,
        id_metodo_pago: int,
        fecha_pago: str,
        monto_pagado: float,
        referencia_pago: str,
        id_estado: int,
    ) -> None:
        if id_pago <= 0:
            raise ValueError("El id del pago es inválido.")

        self.validar_datos(
            id_factura=id_factura,
            id_metodo_pago=id_metodo_pago,
            fecha_pago=fecha_pago,
            monto_pagado=monto_pagado,
            referencia_pago=referencia_pago,
            id_estado=id_estado,
        )

        pago_actual = self.repository.obtener_pago_por_id(id_pago)
        if not pago_actual:
            raise ValueError("El pago que intenta actualizar no existe.")

        referencia_pago = referencia_pago.strip().upper()
        fecha_pago = fecha_pago.strip()

        if (
            referencia_pago != pago_actual.referencia_pago
            and self.repository.existe_referencia_pago(referencia_pago)
        ):
            raise ValueError("Ya existe otro pago registrado con esa referencia.")

        self.repository.actualizar_pago(
            id_pago=id_pago,
            id_factura=id_factura,
            id_metodo_pago=id_metodo_pago,
            fecha_pago=fecha_pago,
            monto_pagado=monto_pagado,
            referencia_pago=referencia_pago,
            id_estado=id_estado,
        )

        logger.info(f"Pago actualizado correctamente. ID={id_pago}")

    def eliminar_pago(self, id_pago: int) -> None:
        if id_pago <= 0:
            raise ValueError("El id del pago es inválido.")

        pago_actual = self.repository.obtener_pago_por_id(id_pago)
        if not pago_actual:
            raise ValueError("El pago que intenta eliminar no existe.")

        self.repository.eliminar_pago(id_pago)
        logger.info(f"Pago eliminado correctamente. ID={id_pago}")