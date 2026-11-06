from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from repositories.solicitudes_repository import SolicitudesRepository
from services.solicitudes_service import SolicitudesService
from fastapi import APIRouter, HTTPException, status
from schemas.solicitudes import SolicitudCreate

router = APIRouter()


@router.post("/solicitudes", status_code=status.HTTP_201_CREATED)
async def crear(solicitud: SolicitudCreate):
    try:
        g = SolicitudesService(SolicitudesRepository())
        
        # Pasamos los datos validados por el esquema Pydantic
        r = g.registrar(
            solicitud.nombre, solicitud.apellido, solicitud.dni, 
            solicitud.email, solicitud.legajo, solicitud.carrera, 
            solicitud.tipo, solicitud.prioridad, solicitud.detalle, 
            solicitud.responsable_id
        )
        
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
        # Reemplazamos el viejo "ok: false" con estado 200 por una excepción 400/500 formal
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )


@router.get("/solicitudes")
def listar(estado: str = None, tipo: str = None, prioridad: str = None, dni: str = None):
    g = SolicitudesService(SolicitudesRepository())     ## S9 - ACOPLAMIENTO FUERTE
    return g.listar(estado, tipo, prioridad, dni)


@router.get("/solicitudes/{id}")
def ver(id: int):
    repo = SolicitudesRepository()   ## S9 - ACOPLAMIENTO FUERTE (accede al repositorio sin pasar por el servicio)
    for s in repo.solicitudes:
        if s["id"] == id:
            return s
    return JSONResponse(status_code=404, content={"msg": "no existe"})


@router.put("/solicitudes/{id}/estado")
async def estado(id: int, request: Request):
    try:
        b = await request.json()
        g = SolicitudesService(SolicitudesRepository())
        r = g.cambiar_estado(id, b["estado"])
        if r == None:
            return JSONResponse(status_code=404, content={"msg": "no existe"})
        if type(r) == str:
            return {"ok": False, "msg": r}
        return {"ok": True, "solicitud": r}
    except:
        return {"ok": False, "msg": "error"}  ## S7 - MANEJO DE ERRORES DEFICIENTE


@router.put("/solicitudes/{id}/responsable")
async def responsable(id: int, request: Request):
    try:
        b = await request.json()
        g = SolicitudesService(SolicitudesRepository())
        r = g.asignar(id, b["responsable_id"])
        if r == None:
            return JSONResponse(status_code=404, content={"msg": "no existe"})
        if type(r) == str:
            return {"ok": False, "msg": r}
        return {"ok": True, "solicitud": r}
    except:
        return {"ok": False, "msg": "error"}  ## S7 - MANEJO DE ERRORES DEFICIENTE
