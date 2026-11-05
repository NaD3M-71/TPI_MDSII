from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from repositories.solicitudes_repository import SolicitudesRepository
from services.solicitudes_service import SolicitudesService

router = APIRouter()


@router.post("/solicitudes")
async def crear(request: Request):
    try:
        b = await request.json()
        g = SolicitudesService(SolicitudesRepository())     ## S9 - ACOPLAMIENTO FUERTE (Instanciación directa en cada endpoint)
        r = g.registrar(b.get("nombre"), b.get("apellido"), b.get("dni"), b.get("email"), b.get("legajo"), b.get("carrera"), b.get("tipo"), b.get("prioridad"), b.get("detalle"), b.get("responsable_id"))
        if type(r) == str:
            return {"ok": False, "msg": r}
        return {"ok": True, "solicitud": r}
    except Exception as e:              ## S7 - MANEJO DE ERRORES DEFICIENTE (Atrapa todo y responde 200 con mensaje genérico)
        return {"ok": False, "msg": "error"}


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
