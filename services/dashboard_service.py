from repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self) -> None:
        self.repository = DashboardRepository()

    def obtener_resumen(self) -> dict:
        row = self.repository.obtener_resumen()

        if not row:
            return {
                "total_clientes": 0,
                "total_empleados": 0,
                "total_autobuses": 0,
                "total_viajes": 0,
                "total_reservaciones": 0,
                "total_facturas": 0,
                "total_pagos": 0,
                "total_facturado": 0.0,
                "total_pagado": 0.0,
            }

        return {
            "total_clientes": int(row.total_clientes),
            "total_empleados": int(row.total_empleados),
            "total_autobuses": int(row.total_autobuses),
            "total_viajes": int(row.total_viajes),
            "total_reservaciones": int(row.total_reservaciones),
            "total_facturas": int(row.total_facturas),
            "total_pagos": int(row.total_pagos),
            "total_facturado": float(row.total_facturado),
            "total_pagado": float(row.total_pagado),
        }