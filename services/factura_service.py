from datetime import datetime

from core.logger import get_logger
from repositories.factura_repository import FacturaRepository


logger = get_logger("FacturaService")


class FacturaService:
    """
    Lógica de negocio del módulo de facturas.
    """

    def __init__(self) -> None:
        self.repository = FacturaRepository()

    # =========================================================
    # CONSULTAS
    # =========================================================
    def listar_facturas(self):
        return self.repository.listar_facturas()

    def obtener_factura_por_id(self, id_factura: int):
        if id_factura <= 0:
            raise ValueError("El id de la factura es inválido.")
        return self.repository.obtener_factura_por_id(id_factura)

    def listar_reservaciones(self):
        return self.repository.listar_reservaciones()

    def listar_descuentos(self):
        return self.repository.listar_descuentos()

    def listar_estados_factura(self):
        return self.repository.listar_estados_factura()

    def obtener_siguiente_id(self) -> int:
        return self.repository.obtener_siguiente_id()
    
    def obtener_siguiente_numero_factura(self) -> str:
        siguiente_id = self.obtener_siguiente_id()
        return f"FAC-{siguiente_id:04d}"

    # =========================================================
    # VALIDACIONES
    # =========================================================
    def validar_datos(
        self,
        id_reservacion: int,
        numero_factura: str,
        fecha_factura: str,
        id_estado: int,
        id_descuento: int | None,
    ) -> None:
        numero_factura = numero_factura.strip()
        fecha_factura = fecha_factura.strip()

        if id_reservacion <= 0:
            raise ValueError("Debe seleccionar una reservación válida.")

        if not numero_factura:
            raise ValueError("El número de factura es obligatorio.")

        if not fecha_factura:
            raise ValueError("La fecha de factura es obligatoria.")

        try:
            datetime.strptime(fecha_factura, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha de factura debe tener formato YYYY-MM-DD.")

        if id_estado <= 0:
            raise ValueError("Debe seleccionar un estado válido.")

        if id_descuento is not None and id_descuento <= 0:
            raise ValueError("El descuento seleccionado no es válido.")

    # =========================================================
    # CÁLCULOS
    # =========================================================
    def calcular_total_con_descuento(
        self,
        subtotal: float,
        impuesto: float,
        total_base: float,
        id_descuento: int | None,
    ) -> float:
        """
        Aplica un descuento simple según el catálogo seleccionado.
        La base del descuento se aplica sobre el subtotal.
        Luego se suma el impuesto ya existente del registro de reservación.
        """
        if subtotal < 0 or impuesto < 0 or total_base < 0:
            raise ValueError("Los montos base de la reservación no son válidos.")

        descuento_porcentaje = 0.0

        if id_descuento == 1:
            descuento_porcentaje = 0.10   # Adulto Mayor
        elif id_descuento == 2:
            descuento_porcentaje = 0.05   # Promoción
        elif id_descuento == 3:
            descuento_porcentaje = 0.08   # Estudiante

        monto_descuento = round(subtotal * descuento_porcentaje, 2)
        nuevo_total = round((subtotal - monto_descuento) + impuesto, 2)

        if id_descuento is None:
            return round(total_base, 2)

        return nuevo_total

    def obtener_montos_reservacion(self, id_reservacion: int) -> tuple[float, float, float]:
        if id_reservacion <= 0:
            raise ValueError("La reservación seleccionada no es válida.")

        row = self.repository.obtener_montos_reservacion(id_reservacion)
        if not row:
            raise ValueError("No se encontraron montos para la reservación seleccionada.")

        subtotal = float(row.subtotal)
        impuesto = float(row.impuestos)
        total = float(row.total)

        return subtotal, impuesto, total

    # =========================================================
    # OPERACIONES
    # =========================================================
    def crear_factura(
        self,
        id_reservacion: int,
        numero_factura: str,
        fecha_factura: str,
        id_descuento: int | None,
        id_estado: int,
    ) -> int:
        self.validar_datos(
            id_reservacion=id_reservacion,
            numero_factura=numero_factura,
            fecha_factura=fecha_factura,
            id_estado=id_estado,
            id_descuento=id_descuento,
        )

        numero_factura = numero_factura.strip().upper()
        fecha_factura = fecha_factura.strip()

        if self.repository.existe_numero_factura(numero_factura):
            raise ValueError("Ya existe una factura registrada con ese número.")

        if self.repository.existe_factura_para_reservacion(id_reservacion):
            raise ValueError("La reservación seleccionada ya tiene una factura asociada.")

        subtotal, impuesto, total_base = self.obtener_montos_reservacion(id_reservacion)
        total_final = self.calcular_total_con_descuento(
            subtotal=subtotal,
            impuesto=impuesto,
            total_base=total_base,
            id_descuento=id_descuento,
        )

        nuevo_id = self.repository.obtener_siguiente_id()

        self.repository.insertar_factura(
            id_factura=nuevo_id,
            id_reservacion=id_reservacion,
            numero_factura=numero_factura,
            fecha_factura=fecha_factura,
            subtotal=subtotal,
            impuesto=impuesto,
            id_descuento=id_descuento,
            total=total_final,
            id_estado=id_estado,
        )

        logger.info(f"Factura creada correctamente. ID={nuevo_id}, Número={numero_factura}")
        return nuevo_id

    def actualizar_factura(
        self,
        id_factura: int,
        id_reservacion: int,
        numero_factura: str,
        fecha_factura: str,
        id_descuento: int | None,
        id_estado: int,
    ) -> None:
        if id_factura <= 0:
            raise ValueError("El id de la factura es inválido.")

        self.validar_datos(
            id_reservacion=id_reservacion,
            numero_factura=numero_factura,
            fecha_factura=fecha_factura,
            id_estado=id_estado,
            id_descuento=id_descuento,
        )

        factura_actual = self.repository.obtener_factura_por_id(id_factura)
        if not factura_actual:
            raise ValueError("La factura que intenta actualizar no existe.")

        numero_factura = numero_factura.strip().upper()
        fecha_factura = fecha_factura.strip()

        if (
            numero_factura != factura_actual.numero_factura
            and self.repository.existe_numero_factura(numero_factura)
        ):
            raise ValueError("Ya existe otra factura registrada con ese número.")

        if (
            id_reservacion != factura_actual.id_reservacion
            and self.repository.existe_factura_para_reservacion(id_reservacion)
        ):
            raise ValueError("La reservación seleccionada ya tiene otra factura asociada.")

        subtotal, impuesto, total_base = self.obtener_montos_reservacion(id_reservacion)
        total_final = self.calcular_total_con_descuento(
            subtotal=subtotal,
            impuesto=impuesto,
            total_base=total_base,
            id_descuento=id_descuento,
        )

        self.repository.actualizar_factura(
            id_factura=id_factura,
            id_reservacion=id_reservacion,
            numero_factura=numero_factura,
            fecha_factura=fecha_factura,
            subtotal=subtotal,
            impuesto=impuesto,
            id_descuento=id_descuento,
            total=total_final,
            id_estado=id_estado,
        )

        logger.info(f"Factura actualizada correctamente. ID={id_factura}")

    def eliminar_factura(self, id_factura: int) -> None:
        if id_factura <= 0:
            raise ValueError("El id de la factura es inválido.")

        factura_actual = self.repository.obtener_factura_por_id(id_factura)
        if not factura_actual:
            raise ValueError("La factura que intenta eliminar no existe.")

        self.repository.eliminar_factura(id_factura)
        logger.info(f"Factura eliminada correctamente. ID={id_factura}")