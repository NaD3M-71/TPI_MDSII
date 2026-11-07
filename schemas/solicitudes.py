from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from models.enums import TipoSolicitud, Prioridad

class SolicitudCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    apellido: str = Field(..., min_length=1)
    dni: str = Field(..., min_length=7, max_length=8)
    email: EmailStr
    legajo: Optional[str] = None
    carrera: Optional[str] = None
    tipo: TipoSolicitud
    prioridad: Prioridad
    detalle: str = Field(..., min_length=10)
    responsable_id: Optional[int] = 0

class SolicitudResponse(BaseModel):
    id: int
    estudiante_id: int
    nombre: str
    apellido: str
    dni: str
    email: str
    legajo: Optional[str] = None
    carrera: Optional[str] = None
    tipo: str
    prioridad: str
    estado: str
    detalle: str
    responsable_id: int
    responsable: str
    fecha: str
    vencimiento: str
    historial: List[str]

class EstadoUpdate(BaseModel):
    estado: str

class ResponsableUpdate(BaseModel):
    responsable_id: int