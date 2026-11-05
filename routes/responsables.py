from fastapi import APIRouter

from repositories.solicitudes_repository import SolicitudesRepository

router = APIRouter()


@router.get("/responsables")
def resps():               ## S12 - NOMBRES POCO DESCRIPTIVOS (Función abreviada)
    repo = SolicitudesRepository()
    return repo.responsables
