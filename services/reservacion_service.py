from datetime import datetime

from core.logger import get_logger
from repositories.reservacion_repository import ReservacionRepository


logger = get_logger("ReservacionService")


class ReservacionService:
    """
    Lógica de negocio del módulo de reservaciones.
    """

    IMPUESTO_PORCENTAJE = 0.13

    def __init__(self) -> None:
        self.repository = ReservacionRepository()

    # =========================================================
    # CONSULTAS
    # =========================================================
    def listar_reservaciones(self):
        return self.repository.listar_reservaciones()

    def obtener_reservacion_por_id(self, id_reservacion: int):
        if id_reservacion <= 0:
            raise ValueError("El id de la reservación es inválido.")
        return self.repository.obtener_reservacion_por_id(id_reservacion)

    def listar_clientes(self):
        return self.repository.listar_clientes()

    def listar_viajes(self):
        return self.repository.listar_viajes()

    def listar_empleados_administrativos(self):
        return self.repository.listar_empleados_administrativos()

    def listar_estados_reservacion(self):
        return self.repository.listar_estados_reservacion()

    def obtener_siguiente_id(self) -> int:
        return self.repository.obtener_siguiente_id()

    # =========================================================
    # VALIDACIONES
    # =========================================================
    def validar_datos(
        self,
        id_cliente: int,
        id_viaje: int,
        id_administrativo: int,
        fecha_reservacion: str,
        cantidad_pasajeros: int,
        id_estado: int,
    ) -> None:
        
        viaje = self.repository.db.execute(
            "SELECT cupo_total FROM VIAJES WHERE id_viaje = ?",
            (id_viaje,),
            fetch_one=True
        )

        cupo_total = int(viaje.cupo_total)
        reservados = self.repository.obtener_pasajeros_reservados(id_viaje)

        if cantidad_pasajeros + reservados > cupo_total:
            raise ValueError("No hay suficiente cupo disponible para este viaje.")

        fecha_reservacion = fecha_reservacion.strip()

        if id_cliente <= 0:
            raise ValueError("Debe seleccionar un cliente válido.")

        if id_viaje <= 0:
            raise ValueError("Debe seleccionar un viaje válido.")

        if id_administrativo <= 0:
            raise ValueError("Debe seleccionar un empleado válido.")

        if not fecha_reservacion:
            raise ValueError("La fecha de reservación es obligatoria.")

        try:
            datetime.strptime(fecha_reservacion, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha de reservación debe tener formato YYYY-MM-DD.")

        if cantidad_pasajeros <= 0:
            raise ValueError("La cantidad de pasajeros debe ser mayor que cero.")

        if cantidad_pasajeros > 100:
            raise ValueError("La cantidad de pasajeros no es válida.")

        if id_estado <= 0:
            raise ValueError("Debe seleccionar un estado válido.")

    # =========================================================
    # CÁLCULOS
    # =========================================================
    def calcular_montos(self, id_viaje: int, cantidad_pasajeros: int) -> tuple[float, float, float]:
        if id_viaje <= 0:
            raise ValueError("El viaje seleccionado no es válido.")

        if cantidad_pasajeros <= 0:
            raise ValueError("La cantidad de pasajeros debe ser mayor que cero.")

        precio_row = self.repository.obtener_precio_base_viaje(id_viaje)
        if not precio_row:
            raise ValueError("No se encontró el precio base del viaje seleccionado.")

        precio_base = float(precio_row.precio_base)
        subtotal = round(precio_base * cantidad_pasajeros, 2)
        impuestos = round(subtotal * self.IMPUESTO_PORCENTAJE, 2)
        total = round(subtotal + impuestos, 2)

        return subtotal, impuestos, total

    # =========================================================
    # OPERACIONES
    # =========================================================
    def crear_reservacion(
        self,
        id_cliente: int,
        id_viaje: int,
        id_administrativo: int,
        fecha_reservacion: str,
        cantidad_pasajeros: int,
        id_estado: int,
    ) -> int:
        self.validar_datos(
            id_cliente=id_cliente,
            id_viaje=id_viaje,
            id_administrativo=id_administrativo,
            fecha_reservacion=fecha_reservacion,
            cantidad_pasajeros=cantidad_pasajeros,
            id_estado=id_estado,
        )

        fecha_reservacion = fecha_reservacion.strip()
        subtotal, impuestos, total = self.calcular_montos(
            id_viaje=id_viaje,
            cantidad_pasajeros=cantidad_pasajeros,
        )

        nuevo_id = self.repository.obtener_siguiente_id()

        self.repository.insertar_reservacion(
            id_reservacion=nuevo_id,
            id_cliente=id_cliente,
            id_viaje=id_viaje,
            id_administrativo=id_administrativo,
            fecha_reservacion=fecha_reservacion,
            cantidad_pasajeros=cantidad_pasajeros,
            subtotal=subtotal,
            impuestos=impuestos,
            total=total,
            id_estado=id_estado,
        )

        logger.info(f"Reservación creada correctamente. ID={nuevo_id}")
        return nuevo_id

    def actualizar_reservacion(
        self,
        id_reservacion: int,
        id_cliente: int,
        id_viaje: int,
        id_administrativo: int,
        fecha_reservacion: str,
        cantidad_pasajeros: int,
        id_estado: int,
    ) -> None:
        if id_reservacion <= 0:
            raise ValueError("El id de la reservación es inválido.")

        self.validar_datos(
            id_cliente=id_cliente,
            id_viaje=id_viaje,
            id_administrativo=id_administrativo,
            fecha_reservacion=fecha_reservacion,
            cantidad_pasajeros=cantidad_pasajeros,
            id_estado=id_estado,
        )

        reservacion_actual = self.repository.obtener_reservacion_por_id(id_reservacion)
        if not reservacion_actual:
            raise ValueError("La reservación que intenta actualizar no existe.")

        fecha_reservacion = fecha_reservacion.strip()
        subtotal, impuestos, total = self.calcular_montos(
            id_viaje=id_viaje,
            cantidad_pasajeros=cantidad_pasajeros,
        )

        self.repository.actualizar_reservacion(
            id_reservacion=id_reservacion,
            id_cliente=id_cliente,
            id_viaje=id_viaje,
            id_administrativo=id_administrativo,
            fecha_reservacion=fecha_reservacion,
            cantidad_pasajeros=cantidad_pasajeros,
            subtotal=subtotal,
            impuestos=impuestos,
            total=total,
            id_estado=id_estado,
        )

        logger.info(f"Reservación actualizada correctamente. ID={id_reservacion}")

    def eliminar_reservacion(self, id_reservacion: int) -> None:
        if id_reservacion <= 0:
            raise ValueError("El id de la reservación es inválido.")

        reservacion_actual = self.repository.obtener_reservacion_por_id(id_reservacion)
        if not reservacion_actual:
            raise ValueError("La reservación que intenta eliminar no existe.")

        self.repository.eliminar_reservacion(id_reservacion)
        logger.info(f"Reservación eliminada correctamente. ID={id_reservacion}")

