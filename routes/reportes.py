from fastapi import APIRouter

from repositories.solicitudes_repository import SolicitudesRepository
from services.solicitudes_service import SolicitudesService

router = APIRouter()


@router.get("/reporte")
def rep():                 ## S12 - NOMBRES POCO DESCRIPTIVOS (Función abreviada)
    g = SolicitudesService(SolicitudesRepository())
    return g.reporte()
