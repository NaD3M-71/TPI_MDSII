from fastapi import APIRouter, Depends, HTTPException, status

from core.dependencies import obtener_servicio_solicitudes
from services.solicitudes_service import SolicitudesService

router = APIRouter(prefix="/responsables", tags=["Responsables"])


@router.get(
    "",
    summary="Listar todos los responsables",
    description="Retorna el listado completo de los responsables registrados en el sistema.",
)
async def listar_responsables(
    servicio: SolicitudesService = Depends(obtener_servicio_solicitudes),
):
    try:
        return servicio.listar_responsables()
    except Exception as error_inesperado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(error_inesperado)}",
        )
