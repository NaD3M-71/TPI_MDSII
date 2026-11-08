import json
import logging
import os

logger = logging.getLogger(__name__)

ARCHIVO_DATOS = "datos.json"


class SolicitudesRepository:
    def __init__(self):
        self.solicitudes = []
        self.estudiantes = []
        self.responsables = [
            {"id": 1, "nombre": "Laura Gomez", "area": "Alumnado"},
            {"id": 2, "nombre": "Carlos Perez", "area": "Titulos"},
            {"id": 3, "nombre": "Marta Diaz", "area": "Bedelia"},
        ]
        # S12 - NOMBRES POCO DESCRIPTIVOS (Se cambió 'cont' y 'cont_est' por nombres descriptivos)
        self.contador_solicitudes = 0
        self.contador_estudiantes = 0

        if os.path.exists(ARCHIVO_DATOS):
            try:
                # S12 - NOMBRES POCO DESCRIPTIVOS (Se cambió 'f' y 'd' por 'archivo' y 'contenido_json')
                with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
                    contenido_json = json.loads(archivo.read())
                    self.solicitudes = contenido_json.get("solicitudes", [])
                    self.estudiantes = contenido_json.get("estudiantes", [])
                    self.contador_solicitudes = contenido_json.get(
                        "contador_solicitudes", 0
                    )
                    self.contador_estudiantes = contenido_json.get(
                        "contador_estudiantes", 0
                    )
            except (json.JSONDecodeError, OSError) as error_lectura:
                # S7 - MANEJO DE ERRORES DEFICIENTE (Se reemplazó el except vacío por captura y log)
                logger.error(
                    "Error al cargar los datos desde el archivo: %s", error_lectura
                )

    def guardar(self):
        try:
            datos_a_guardar = {
                "solicitudes": self.solicitudes,
                "estudiantes": self.estudiantes,
                "contador_solicitudes": self.contador_solicitudes,
                "contador_estudiantes": self.contador_estudiantes,
            }
            with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
                archivo.write(json.dumps(datos_a_guardar, ensure_ascii=False, indent=4))
        except OSError as error_escritura:
            # S7 - MANEJO DE ERRORES DEFICIENTE (Se reemplazó el except vacío por captura y log)
            logger.error(
                "Error al guardar los datos en el archivo: %s", error_escritura
            )
