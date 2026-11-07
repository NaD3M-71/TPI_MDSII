from fastapi import APIRouter, Depends, HTTPException, status

from core.dependencies import obtener_servicio_solicitudes
from schemas.solicitudes import EstadoUpdate, ResponsableUpdate, SolicitudCreate
from services.solicitudes_service import SolicitudesService

# S9 - ACOPLAMIENTO FUERTE (Se centralizan los routers modularizados)
router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una nueva solicitud",
    description="Crea una solicitud académica validando datos mediante DTOs y reglas de negocio.",
)
async def crear_solicitud(
    solicitud: SolicitudCreate,
    # S9 - Eliminación de acoplamiento fuerte mediante Inyección de Dependencias (DI)
    # y centralización de la creacion de servicios en dependencies.py
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # S7 - MEJORA EN MANEJO DE ERRORES ( ahora evitamos excepciones genéricas silenciosas)
            detail=f"Error interno: {str(error_inesperado)}",
        )


@router.get(
    "",
    summary="Listar solicitudes con filtros opcionales",
    description="Permite filtrar las solicitudes por estado, tipo, prioridad o DNI.",
)
def listar_solicitudes(
    estado: str = None,
    tipo: str = None,
    prioridad: str = None,
    dni: str = None,
    servicio: SolicitudesService = Depends(obtener_servicio_solicitudes),
):
    try:
        return servicio.listar(estado, tipo, prioridad, dni)
    except Exception as error_inesperado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(error_inesperado)}",
        )


@router.get(
    "/{id}",
    summary="Ver detalle de una solicitud por ID",
    description="Busca y retorna una solicitud específica según su identificador único.",
)
def ver_solicitud(
    id: int, servicio: SolicitudesService = Depends(obtener_servicio_solicitudes)
):
    solicitudes = servicio.listar(servicio)
    for solicitud in solicitudes:
        if solicitud.get("id") == id:
            return solicitud
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No existe la solicitud"
    )


@router.put(
    "/{id}/estado",
    summary="Cambiar el estado de una solicitud",
    description="Actualiza el estado actual de una solicitud existente.",
)
async def cambiar_estado_solicitud(
    id: int,
    datos_estado: EstadoUpdate,  # S12 - NOMBRES DESCRIPTIVOS
    servicio: SolicitudesService = Depends(obtener_servicio_solicitudes),
):
    try:
        resultado = servicio.cambiar_estado(id, datos_estado.estado)

        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No existe la solicitud"
            )
        if isinstance(resultado, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=resultado
            )

        return resultado

    except HTTPException as error_http:
        raise error_http
    except Exception as error_inesperado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(error_inesperado)}",
        )


@router.put(
    "/{id}/responsable",
    summary="Asignar responsable a una solicitud",
    description="Modifica o asigna el ID del responsable encargado de la solicitud.",
)
async def responsable(
    id: int,
    datos_responsable: ResponsableUpdate,
    servicio: SolicitudesService = Depends(obtener_servicio_solicitudes),
):
    try:
        resultado = servicio.asignar(id, datos_responsable.responsable_id)

        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No existe la solicitud"
            )
        if isinstance(resultado, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=resultado
            )

        return resultado

    except HTTPException as error_http:
        raise error_http
    except Exception as error_inesperado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(error_inesperado)}",
        )
