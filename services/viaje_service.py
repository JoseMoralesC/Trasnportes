from datetime import datetime

from core.logger import get_logger
from repositories.viaje_repository import ViajeRepository


logger = get_logger("ViajeService")


class ViajeService:
    """
    Lógica de negocio del módulo de viajes.
    """

    def __init__(self) -> None:
        self.repository = ViajeRepository()

    # =========================================================
    # CONSULTAS
    # =========================================================
    def listar_viajes(self):
        return self.repository.listar_viajes()

    def obtener_viaje_por_id(self, id_viaje: int):
        if id_viaje <= 0:
            raise ValueError("El id del viaje es inválido.")
        return self.repository.obtener_viaje_por_id(id_viaje)

    def listar_rutas(self):
        return self.repository.listar_rutas()

    def listar_autobuses(self):
        return self.repository.listar_autobuses()

    def listar_precios_base(self):
        return self.repository.listar_precios_base()

    def listar_estados_viaje(self):
        return self.repository.listar_estados_viaje()

    def obtener_siguiente_id(self) -> int:
        return self.repository.obtener_siguiente_id()

    # =========================================================
    # VALIDACIONES
    # =========================================================
    def validar_datos(
        self,
        id_ruta: int,
        id_autobus: int,
        fecha_salida: str,
        hora_salida: str,
        id_precio: int,
        cupo_total: int,
        id_estado: int,
    ) -> None:
        fecha_salida = fecha_salida.strip()
        hora_salida = hora_salida.strip()

        if id_ruta <= 0:
            raise ValueError("Debe seleccionar una ruta válida.")

        if id_autobus <= 0:
            raise ValueError("Debe seleccionar un autobús válido.")

        if not fecha_salida:
            raise ValueError("La fecha de salida es obligatoria.")

        if not hora_salida:
            raise ValueError("La hora de salida es obligatoria.")

        try:
            datetime.strptime(fecha_salida, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha de salida debe tener formato YYYY-MM-DD.")

        try:
            datetime.strptime(hora_salida, "%H:%M")
        except ValueError:
            try:
                datetime.strptime(hora_salida, "%H:%M:%S")
            except ValueError:
                raise ValueError("La hora de salida debe tener formato HH:MM o HH:MM:SS.")

        if id_precio <= 0:
            raise ValueError("Debe seleccionar un precio base válido.")

        if cupo_total <= 0:
            raise ValueError("El cupo total debe ser mayor que cero.")

        if cupo_total > 100:
            raise ValueError("El cupo total no es válido.")

        if id_estado <= 0:
            raise ValueError("Debe seleccionar un estado válido.")

    # =========================================================
    # HELPERS
    # =========================================================
    def normalizar_hora(self, hora_salida: str) -> str:
        hora_salida = hora_salida.strip()

        try:
            parsed = datetime.strptime(hora_salida, "%H:%M")
            return parsed.strftime("%H:%M:%S")
        except ValueError:
            parsed = datetime.strptime(hora_salida, "%H:%M:%S")
            return parsed.strftime("%H:%M:%S")

    # =========================================================
    # OPERACIONES
    # =========================================================
    def crear_viaje(
        self,
        id_ruta: int,
        id_autobus: int,
        fecha_salida: str,
        hora_salida: str,
        id_precio: int,
        cupo_total: int,
        id_estado: int,
    ) -> int:
        self.validar_datos(
            id_ruta=id_ruta,
            id_autobus=id_autobus,
            fecha_salida=fecha_salida,
            hora_salida=hora_salida,
            id_precio=id_precio,
            cupo_total=cupo_total,
            id_estado=id_estado,
        )

        fecha_salida = fecha_salida.strip()
        hora_salida = self.normalizar_hora(hora_salida)

        nuevo_id = self.repository.obtener_siguiente_id()

        self.repository.insertar_viaje(
            id_viaje=nuevo_id,
            id_ruta=id_ruta,
            id_autobus=id_autobus,
            fecha_salida=fecha_salida,
            hora_salida=hora_salida,
            id_precio=id_precio,
            cupo_total=cupo_total,
            id_estado=id_estado,
        )

        logger.info(f"Viaje creado correctamente. ID={nuevo_id}")
        return nuevo_id

    def actualizar_viaje(
        self,
        id_viaje: int,
        id_ruta: int,
        id_autobus: int,
        fecha_salida: str,
        hora_salida: str,
        id_precio: int,
        cupo_total: int,
        id_estado: int,
    ) -> None:
        if id_viaje <= 0:
            raise ValueError("El id del viaje es inválido.")

        self.validar_datos(
            id_ruta=id_ruta,
            id_autobus=id_autobus,
            fecha_salida=fecha_salida,
            hora_salida=hora_salida,
            id_precio=id_precio,
            cupo_total=cupo_total,
            id_estado=id_estado,
        )

        viaje_actual = self.repository.obtener_viaje_por_id(id_viaje)
        if not viaje_actual:
            raise ValueError("El viaje que intenta actualizar no existe.")

        fecha_salida = fecha_salida.strip()
        hora_salida = self.normalizar_hora(hora_salida)

        self.repository.actualizar_viaje(
            id_viaje=id_viaje,
            id_ruta=id_ruta,
            id_autobus=id_autobus,
            fecha_salida=fecha_salida,
            hora_salida=hora_salida,
            id_precio=id_precio,
            cupo_total=cupo_total,
            id_estado=id_estado,
        )

        logger.info(f"Viaje actualizado correctamente. ID={id_viaje}")

    def eliminar_viaje(self, id_viaje: int) -> None:
        if id_viaje <= 0:
            raise ValueError("El id del viaje es inválido.")

        viaje_actual = self.repository.obtener_viaje_por_id(id_viaje)
        if not viaje_actual:
            raise ValueError("El viaje que intenta eliminar no existe.")

        self.repository.eliminar_viaje(id_viaje)
        logger.info(f"Viaje eliminado correctamente. ID={id_viaje}")