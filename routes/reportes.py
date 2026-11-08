from fastapi import APIRouter, Depends, HTTPException, status

from core.dependencies import obtener_servicio_solicitudes
from services.solicitudes_service import SolicitudesService

router = APIRouter(prefix="/reporte", tags=["Reportes"])


@router.get(
    "",
    summary="Obtener reporte general de solicitudes",
    description="Genera y retorna métricas y un resumen estadístico del estado actual de las solicitudes.",
)
async def obtener_reporte(
    servicio: SolicitudesService = Depends(obtener_servicio_solicitudes),
):
    try:
        return servicio.reporte()
    except Exception as error_inesperado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(error_inesperado)}",
        )
