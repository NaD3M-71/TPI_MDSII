from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse

from repositories.solicitudes_repository import SolicitudesRepository
from services.solicitudes_service import SolicitudesService
from schemas.solicitudes import SolicitudCreate

router = APIRouter()


@router.post("/solicitudes", status_code=status.HTTP_201_CREATED)
async def crear(solicitud: SolicitudCreate):
    try:
        g = SolicitudesService(SolicitudesRepository())
        
        # Pasamos el objeto solicitud completo (o solicitud.model_dump() / solicitud.dict() según corresponda)
        r = g.registrar(solicitud)
        
        # Si el servicio retorna un string de error de negocio, lanzamos 400 Bad Request
        if isinstance(r, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=r
            )
            
        return {"ok": True, "solicitud": r}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )


@router.get("/solicitudes")
def listar(estado: str = None, tipo: str = None, prioridad: str = None, dni: str = None):
    g = SolicitudesService(SolicitudesRepository())    ## S9 - ACOPLAMIENTO FUERTE
    return g.listar(estado, tipo, prioridad, dni)


@router.get("/solicitudes/{id}")
def ver(id: int):
    repo = SolicitudesRepository()   ## S9 - ACOPLAMIENTO FUERTE (accede al repositorio sin pasar por el servicio)
    for s in repo.solicitudes:
        if s["id"] == id:
            return s
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe la solicitud")


@router.put("/solicitudes/{id}/estado")
async def estado(id: int, request: Request):
    try:
        b = await request.json()
        g = SolicitudesService(SolicitudesRepository())
        r = g.cambiar_estado(id, b.get("estado"))
        
        if r is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No existe la solicitud"
            )
        if isinstance(r, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=r
            )
            
        return {"ok": True, "solicitud": r}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )


@router.put("/solicitudes/{id}/responsable")
async def responsable(id: int, request: Request):
    try:
        b = await request.json()
        g = SolicitudesService(SolicitudesRepository())
        r = g.asignar(id, b.get("responsable_id"))
        
        if r is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No existe la solicitud"
            )
        if isinstance(r, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=r
            )
            
        return {"ok": True, "solicitud": r}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )
