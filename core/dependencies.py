# dependencies.py
from repositories.solicitudes_repository import SolicitudesRepository
from services.solicitudes_service import SolicitudesService

# S9 - ACOPLAMIENTO FUERTE (Composition Root / Patrón Factory)
# Este módulo centraliza la inyección de dependencias para evitar que los routers
# instancien directamente los repositorios o servicios, desacoplando las capas
# y facilitando la creacion de mocks para futuras pruebas unitarias.


def obtener_servicio_solicitudes() -> SolicitudesService:
    """Función centralizada para inyectar el servicio con su repositorio."""
    repositorio = SolicitudesRepository()
    return SolicitudesService(repositorio)
