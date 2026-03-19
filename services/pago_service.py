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

    def obtener_nombre_metodo_pago(self, id_metodo_pago: int) -> str:
        """
        Retorna el nombre del método de pago según su ID.
        Se usa como compatibilidad para flujos antiguos y validaciones.
        """
        metodos = {
            1: "Efectivo",
            2: "Debito",
            3: "Credito",
            4: "SINPE",
            5: "Transf",
            6: "Deposito",
            7: "Pago web",
            8: "PayPal",
            9: "Link pago",
            10: "Datafono",
            11: "Cheque",
            12: "CredInt",
            13: "Puntos",
            14: "QR bank",
            15: "Mixto",
        }

        nombre = metodos.get(id_metodo_pago)
        if not nombre:
            raise ValueError(
                f"No existe un método de pago configurado para el ID: {id_metodo_pago}"
            )

        return nombre

    def obtener_prefijo_referencia(self, metodo_pago: str) -> str:
        """
        Devuelve el prefijo correspondiente según el nombre del método de pago.
        Se mantiene por compatibilidad, pero la opción recomendada es usar
        obtener_prefijo_referencia_por_id().
        """
        metodo_normalizado = (metodo_pago or "").strip().lower()

        mapa_prefijos = {
            "efectivo": "REF-EFEC-",
            "debito": "REF-DEBI-",
            "credito": "REF-CRED-",
            "sinpe": "REF-SINP-",
            "transf": "REF-TRAN-",
            "deposito": "REF-DEPO-",
            "pago web": "REF-WEB-",
            "paypal": "REF-PAYP-",
            "link pago": "REF-LINK-",
            "datafono": "REF-DATA-",
            "cheque": "REF-CHEQ-",
            "credint": "REF-CINT-",
            "puntos": "REF-PUNT-",
            "qr bank": "REF-QRBK-",
            "mixto": "REF-MIXT-",
            "tarjeta": "REF-TARJ-",
            "transferencia": "REF-TRANS-",
        }

        prefijo = mapa_prefijos.get(metodo_normalizado)
        if not prefijo:
            raise ValueError(
                f"No se pudo determinar el prefijo para el método de pago seleccionado: {metodo_pago}"
            )

        return prefijo

    def obtener_prefijo_referencia_por_id(self, id_metodo_pago: int) -> str:
        """
        Retorna el prefijo según el ID del método de pago.
        Esta es la forma más robusta de trabajar.
        """
        prefijos = {
            1: "REF-EFEC-",
            2: "REF-DEBI-",
            3: "REF-CRED-",
            4: "REF-SINP-",
            5: "REF-TRAN-",
            6: "REF-DEPO-",
            7: "REF-WEB-",
            8: "REF-PAYP-",
            9: "REF-LINK-",
            10: "REF-DATA-",
            11: "REF-CHEQ-",
            12: "REF-CINT-",
            13: "REF-PUNT-",
            14: "REF-QRBK-",
            15: "REF-MIXT-",
        }

        prefijo = prefijos.get(id_metodo_pago)
        if not prefijo:
            raise ValueError(
                f"No hay prefijo configurado para el método de pago con ID: {id_metodo_pago}"
            )

        return prefijo

    def generar_referencia_pago(self, id_metodo_pago: int) -> str:
        """
        Genera una nueva referencia automática según el método de pago.
        Ejemplo:
        - Efectivo -> REF-EFEC-0001
        - Debito   -> REF-DEBI-0001
        - SINPE    -> REF-SINP-0001
        """
        prefijo = self.obtener_prefijo_referencia_por_id(id_metodo_pago)

        ultimo_numero = self.repository.obtener_ultimo_numero_referencia_por_prefijo(prefijo)
        siguiente_numero = ultimo_numero + 1

        return f"{prefijo}{siguiente_numero:04d}"

    def referencia_corresponde_a_metodo(self, id_metodo_pago: int, referencia_pago: str) -> bool:
        """
        Valida que la referencia coincida con el prefijo esperado
        según el método de pago seleccionado.
        """
        prefijo_esperado = self.obtener_prefijo_referencia_por_id(id_metodo_pago)
        referencia_normalizada = (referencia_pago or "").strip().upper()

        return referencia_normalizada.startswith(prefijo_esperado)

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
        fecha_pago = (fecha_pago or "").strip()
        referencia_pago = (referencia_pago or "").strip().upper()

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
            raise ValueError(
                "La referencia de pago no corresponde al método de pago seleccionado."
            )

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