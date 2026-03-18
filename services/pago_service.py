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
    # HELPERS
    # =========================================================
    def obtener_total_factura(self, id_factura: int) -> float:
        if id_factura <= 0:
            raise ValueError("La factura seleccionada no es válida.")

        row = self.repository.obtener_total_factura(id_factura)
        if not row:
            raise ValueError("No se encontró el total de la factura seleccionada.")

        return float(row.total)

    def obtener_prefijo_referencia(self, metodo_pago: str) -> str:
        """
        Devuelve el prefijo correspondiente según el método de pago.
        """
        metodo_normalizado = (metodo_pago or "").strip().lower()

        mapa_prefijos = {
            "tarjeta": "REF-TARJ-",
            "efectivo": "REF-EFEC-",
            "transferencia": "REF-TRANS-",
        }

        prefijo = mapa_prefijos.get(metodo_normalizado)
        if not prefijo:
            raise ValueError("No se pudo determinar el prefijo para el método de pago seleccionado.")

        return prefijo

    def obtener_nombre_metodo_pago(self, id_metodo_pago: int) -> str:
        """
        Busca el nombre del método de pago a partir del id.
        """
        if id_metodo_pago <= 0:
            raise ValueError("El método de pago es inválido.")

        metodos = self.listar_metodos_pago()
        for metodo in metodos:
            if int(metodo.id_metodo_pago) == int(id_metodo_pago):
                return str(metodo.nombre_metodo).strip()

        raise ValueError("No se encontró el método de pago seleccionado.")

    def generar_referencia_pago(self, id_metodo_pago: int) -> str:
        """
        Genera una nueva referencia automática según el método de pago:
        - Tarjeta       -> REF-TARJ-0001
        - Efectivo      -> REF-EFEC-0001
        - Transferencia -> REF-TRANS-0001
        """
        nombre_metodo = self.obtener_nombre_metodo_pago(id_metodo_pago)
        prefijo = self.obtener_prefijo_referencia(nombre_metodo)

        ultimo_numero = self.repository.obtener_ultimo_numero_referencia_por_prefijo(prefijo)
        siguiente_numero = ultimo_numero + 1

        return f"{prefijo}{siguiente_numero:04d}"

    def referencia_corresponde_a_metodo(self, id_metodo_pago: int, referencia_pago: str) -> bool:
        """
        Valida que la referencia coincida con el prefijo esperado
        según el método de pago.
        """
        nombre_metodo = self.obtener_nombre_metodo_pago(id_metodo_pago)
        prefijo = self.obtener_prefijo_referencia(nombre_metodo)
        referencia_normalizada = (referencia_pago or "").strip().upper()

        return referencia_normalizada.startswith(prefijo)

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
        referencia_pago = referencia_pago.strip().upper()

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

        if not self.referencia_corresponde_a_metodo(id_metodo_pago, referencia_pago):
            raise ValueError("La referencia de pago no corresponde al método de pago seleccionado.")

        if id_estado <= 0:
            raise ValueError("Debe seleccionar un estado válido.")

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

        pago_actual = self.repository.obtener_pago_por_id(id_pago)
        if not pago_actual:
            raise ValueError("El pago que intenta actualizar no existe.")

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

        if (
            referencia_pago != str(pago_actual.referencia_pago).strip().upper()
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