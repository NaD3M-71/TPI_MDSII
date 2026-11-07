import datetime
from typing import ClassVar
from models.enums import TipoSolicitud, Prioridad

# REFACTORIZACIÓN SRP (Single Responsibility) y S3 (Long Method)

# Se extrajo el cálculo de plazos y vencimientos fuera del servicio principal.
# Esta clase tiene una única responsabilidad: calcular los días de vencimiento 
# según el tipo de solicitud y su prioridad.

class CalculadoraPlazos:
    PLAZOS_POR_TIPO: ClassVar[dict] = {
        TipoSolicitud.CERTIFICADO: 5,
        TipoSolicitud.EQUIVALENCIA: 30,
        TipoSolicitud.RECLAMO: 10
    }
    
    ESTRATEGIA_PRIORIDAD: ClassVar[dict] = {
        Prioridad.ALTA: lambda dias: dias // 2,
        Prioridad.MEDIA: lambda dias: dias,
        Prioridad.BAJA: lambda dias: dias + 5
    }

    @classmethod
    def calcular_vencimiento(cls, tipo: TipoSolicitud, prioridad: Prioridad) -> datetime.datetime:
        plazo_base = cls.PLAZOS_POR_TIPO.get(tipo, 15)
        estrategia = cls.ESTRATEGIA_PRIORIDAD.get(prioridad, lambda d: d)
        plazo_final = estrategia(plazo_base)
        return datetime.datetime.now() + datetime.timedelta(days=plazo_final)