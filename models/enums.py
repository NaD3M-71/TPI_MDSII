from enum import Enum

# Se reemplazan los strings mágicos sueltos ("certificado", "alta", "pendiente") 
# por Enums tipados, garantizando seguridad de tipos y un dominio acotado.

class TipoSolicitud(str, Enum):
    CERTIFICADO = "certificado"
    EQUIVALENCIA = "equivalencia"
    RECLAMO = "reclamo"

class Prioridad(str, Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

class EstadoSolicitud(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en proceso"
    RESUELTA = "resuelta"