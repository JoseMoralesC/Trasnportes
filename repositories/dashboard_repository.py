from core.db_manager import DBManager


class DashboardRepository:
    def __init__(self) -> None:
        self.db = DBManager()

    def obtener_resumen(self):
        query = """
        SELECT
            (SELECT COUNT(*) FROM CLIENTES) AS total_clientes,
            (SELECT COUNT(*) FROM EMPLEADOS) AS total_empleados,
            (SELECT COUNT(*) FROM AUTOBUSES) AS total_autobuses,
            (SELECT COUNT(*) FROM VIAJES) AS total_viajes,
            (SELECT COUNT(*) FROM RESERVACIONES) AS total_reservaciones,
            (SELECT COUNT(*) FROM FACTURAS) AS total_facturas,
            (SELECT COUNT(*) FROM PAGOS) AS total_pagos,
            (SELECT ISNULL(SUM(total), 0) FROM FACTURAS) AS total_facturado,
            (SELECT ISNULL(SUM(monto_pagado), 0) FROM PAGOS) AS total_pagado;
        """
        return self.db.execute(query, fetch_one=True)