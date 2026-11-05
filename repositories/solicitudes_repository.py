import json
import os

ARCH = "datos.json"


class SolicitudesRepository:
    def __init__(self):
        self.solicitudes = []
        self.estudiantes = []
        self.responsables = [
            {"id": 1, "nombre": "Laura Gomez", "area": "Alumnado"},
            {"id": 2, "nombre": "Carlos Perez", "area": "Titulos"},
            {"id": 3, "nombre": "Marta Diaz", "area": "Bedelia"},
        ]
        self.cont = 0
        self.cont_est = 0
        if os.path.exists(ARCH):
            try:
                f = open(ARCH, "r")
                d = json.loads(f.read())
                self.solicitudes = d["solicitudes"]
                self.estudiantes = d["estudiantes"]
                self.cont = d["cont"]
                self.cont_est = d["cont_est"]
            except: 
                pass    ## S7 - MANEJO DE ERRORES DEFICIENTE (except vacío)

    def guardar(self):
        try:
            f = open(ARCH, "w")
            f.write(json.dumps({"solicitudes": self.solicitudes, "estudiantes": self.estudiantes, "cont": self.cont, "cont_est": self.cont_est}))
        except:
            pass        ## S7 - MANEJO DE ERRORES DEFICIENTE (except vacío)
