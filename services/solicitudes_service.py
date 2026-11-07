import datetime
from typing import ClassVar

from models.enums import EstadoSolicitud, Prioridad, TipoSolicitud
from repositories.solicitudes_repository import SolicitudesRepository
from schemas.solicitudes import SolicitudCreate
from services.calculadora_plazos import CalculadoraPlazos

# REFACTORIZACIÓN OCP (Open/Closed Principle) y RUF012

# Se define la tabla de transiciones válidas como tuplas inmutables tipadas con ClassVar,
# eliminando los complejos if/else anidados y permitiendo extender estados sin modificar la lógica.


class SolicitudesService:
    TRANSICIONES_VALIDAS: ClassVar[dict] = {
        EstadoSolicitud.PENDIENTE: (
            EstadoSolicitud.EN_PROCESO,
            EstadoSolicitud.RESUELTA,
        ),
        EstadoSolicitud.EN_PROCESO: (EstadoSolicitud.RESUELTA,),
        EstadoSolicitud.RESUELTA: (),
    }

    # S9 - INVERSIÓN DE DEPENDENCIAS (Recibe el repositorio por parámetro en lugar de acoplarlo)
    def __init__(self, repo: SolicitudesRepository = None):
        self.repo = repo

    def registrar(self, data: SolicitudCreate) -> dict:
        tipo = TipoSolicitud(data.tipo.lower())
        prioridad = Prioridad(data.prioridad.lower())

        # Delegación de responsabilidades a métodos auxiliares privados y helpers
        estudiante_id = self._obtener_o_crear_estudiante(data)
        vencimiento = CalculadoraPlazos.calcular_vencimiento(tipo, prioridad)

        self.repo.contador_solicitudes += 1
        nombre_resp, id_resp = self._buscar_responsable(data.responsable_id)

        ahora = datetime.datetime.now()
        timestamp = ahora.strftime("%d/%m/%Y %H:%M")

        nueva_solicitud = {
            "id": self.repo.contador_solicitudes,
            "estudiante_id": estudiante_id,
            "nombre": data.nombre,
            "apellido": data.apellido,
            "dni": str(data.dni),
            "email": data.email,
            "legajo": data.legajo,
            "carrera": data.carrera,
            "tipo": tipo.value,
            "prioridad": prioridad.value,
            "estado": EstadoSolicitud.PENDIENTE.value,
            "detalle": data.detalle,
            "responsable_id": id_resp,
            "responsable": nombre_resp,
            "fecha": ahora.strftime("%d/%m/%Y"),
            "vencimiento": vencimiento.strftime("%d/%m/%Y"),
            "historial": [f"{EstadoSolicitud.PENDIENTE.value} {timestamp}"],
        }

        self.repo.solicitudes.append(nueva_solicitud)
        self.repo.guardar()
        return nueva_solicitud

    def cambiar_estado(self, id: int, nuevo_estado_str: str) -> dict:
        try:
            nuevo_estado = EstadoSolicitud(nuevo_estado_str.lower())
        except ValueError:
            return "error estado"

        solicitud = self._buscar_solicitud_por_id(id)
        if not solicitud:
            return None

        estado_actual = EstadoSolicitud(solicitud["estado"])

        if estado_actual == EstadoSolicitud.RESUELTA:
            return "error ya resuelta"

        if (
            nuevo_estado == EstadoSolicitud.EN_PROCESO
            and solicitud["responsable_id"] == 0
        ):
            return "error sin responsable"

        # Validación limpia consultando la tabla de transiciones en lugar de anidar ifs
        if nuevo_estado not in self.TRANSICIONES_VALIDAS.get(estado_actual, []):
            return "error transicion"

        solicitud["estado"] = nuevo_estado.value
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        solicitud["historial"].append(f"{nuevo_estado.value} {timestamp}")

        self.repo.guardar()
        return solicitud

    def asignar(self, id: int, responsable_id: int) -> dict:
        solicitud = self._buscar_solicitud_por_id(id)
        if not solicitud:
            return None

        nombre_resp, id_encontrado = self._buscar_responsable(responsable_id)
        if id_encontrado == 0:
            return "error responsable"

        solicitud["responsable_id"] = id_encontrado
        solicitud["responsable"] = nombre_resp
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        solicitud["historial"].append(f"asignada a {nombre_resp} {timestamp}")

        self.repo.guardar()
        return solicitud

        # REFACTORIZACIÓN S6 (Código Duplicado)

        # Se reemplazan los bloques repetidos de filtros manuales por una
        # comprensión de listas declarativa limpia y en una sola pasada.

    def listar(
        self,
        estado: str = None,
        tipo: str = None,
        prioridad: str = None,
        dni: str = None,
    ) -> list:
        return [
            s
            for s in self.repo.solicitudes
            if (not estado or s["estado"] == estado)
            and (not tipo or s["tipo"] == tipo)
            and (not prioridad or s["prioridad"] == prioridad)
            and (not dni or s["dni"] == dni)
        ]

    def reporte(self) -> dict:
        solicitudes = self.repo.solicitudes
        total = len(solicitudes)

        if total == 0:
            return {
                "total": 0,
                "pendiente": 0,
                "en proceso": 0,
                "resuelta": 0,
                "porc_resueltas": 0,
                "alta_sin_resolver": 0,
            }

        conteo = {
            EstadoSolicitud.PENDIENTE.value: sum(
                1 for s in solicitudes if s["estado"] == EstadoSolicitud.PENDIENTE.value
            ),
            EstadoSolicitud.EN_PROCESO.value: sum(
                1
                for s in solicitudes
                if s["estado"] == EstadoSolicitud.EN_PROCESO.value
            ),
            EstadoSolicitud.RESUELTA.value: sum(
                1 for s in solicitudes if s["estado"] == EstadoSolicitud.RESUELTA.value
            ),
        }

        alta_sin_resolver = sum(
            1
            for s in solicitudes
            if s["prioridad"] == Prioridad.ALTA.value
            and s["estado"] != EstadoSolicitud.RESUELTA.value
        )

        resueltas = conteo[EstadoSolicitud.RESUELTA.value]

        return {
            "total": total,
            "pendiente": conteo[EstadoSolicitud.PENDIENTE.value],
            "en proceso": conteo[EstadoSolicitud.EN_PROCESO.value],
            "resuelta": resueltas,
            "porc_resueltas": round(resueltas * 100 / total, 2),
            "alta_sin_resolver": alta_sin_resolver,
        }

    # REFACTORIZACIÓN S2 (Long Method) y SRP

    # Métodos privados auxiliares de baja complejidad ciclomática
    # para mantener los métodos públicos cortos y altamente cohesivos.

    def _buscar_solicitud_por_id(self, id: int):
        for s in self.repo.solicitudes:
            if s["id"] == id:
                return s
        return None

    def _obtener_o_crear_estudiante(self, data: SolicitudCreate) -> int:
        for estudiante in self.repo.estudiantes:
            if estudiante["dni"] == str(data.dni):
                return estudiante["id"]

        self.repo.contador_estudiantes += 1
        nuevo_estudiante = {
            "id": self.repo.contador_estudiantes,
            "nombre": data.nombre,
            "apellido": data.apellido,
            "dni": str(data.dni),
            "email": data.email,
            "legajo": data.legajo,
            "carrera": data.carrera,
        }
        self.repo.estudiantes.append(nuevo_estudiante)
        return self.repo.contador_estudiantes

    def _buscar_responsable(self, responsable_id: int):
        if not responsable_id:
            return "", 0
        for r in self.repo.responsables:
            if r["id"] == responsable_id:
                return r["nombre"], r["id"]
        return "", 0

    def listar_responsables(self) -> list:
        return self.repo.responsables
