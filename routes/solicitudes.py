from fastapi import APIRouter, Depends, HTTPException, Request, status

from repositories.solicitudes_repository import SolicitudesRepository
from schemas.solicitudes import SolicitudCreate
from services.solicitudes_service import SolicitudesService

router = APIRouter()


# Función de dependencia para evitar el acoplamiento
def obtener_servicio_solicitudes() -> SolicitudesService:
    repositorio = SolicitudesRepository()
    return SolicitudesService(repositorio)


@router.post(
    "/solicitudes",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una nueva solicitud",
    description="Crea una solicitud académica validando datos mediante DTOs y reglas de negocio.",
)
async def crear_solicitud(
    solicitud: SolicitudCreate,
    servicio: SolicitudesService = Depends(obtener_servicio_solicitudes),
):
    try:
        resultado_registro = servicio.registrar(solicitud)

        # Si el servicio retorna un string de error de negocio, lanzamos 400 Bad Request
        if isinstance(resultado_registro, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=resultado_registro
            )

        return resultado_registro  # enfoque REST: devuelve el recurso directamente en lugar del diccionario con la estructura {"ok": True)

    except HTTPException as error_http:
        raise error_http
    except Exception as error_inesperado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(error_inesperado)}",
        )


@router.get("/solicitudes")
def listar(
    estado: str = None, tipo: str = None, prioridad: str = None, dni: str = None
):
    g = SolicitudesService(SolicitudesRepository())  ## S9 - ACOPLAMIENTO FUERTE
    return g.listar(estado, tipo, prioridad, dni)


@router.get("/solicitudes/{id}")
def ver(id: int):
    repo = (
        SolicitudesRepository()
    )  ## S9 - ACOPLAMIENTO FUERTE (accede al repositorio sin pasar por el servicio)
    for s in repo.solicitudes:
        if s["id"] == id:
            return s
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No existe la solicitud"
    )


@router.put("/solicitudes/{id}/estado")
async def estado(id: int, request: Request):
    try:
        b = await request.json()
        g = SolicitudesService(
            SolicitudesRepository()
        )  ## S9 - ACOPLAMIENTO FUERTE (Instanciación directa en cada endpoint)
        r = g.cambiar_estado(id, b.get("estado"))

        if r is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No existe la solicitud"
            )
        if isinstance(r, str):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=r)

        return {"ok": True, "solicitud": r}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/solicitudes/{id}/responsable")
async def responsable(id: int, request: Request):
    try:
        b = await request.json()
        g = SolicitudesService(
            SolicitudesRepository()
        )  ## S9 - ACOPLAMIENTO FUERTE (Instanciación directa en cada endpoint)
        r = g.asignar(id, b.get("responsable_id"))

        if r is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No existe la solicitud"
            )
        if isinstance(r, str):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=r)

        return {"ok": True, "solicitud": r}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
