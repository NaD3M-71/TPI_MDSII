import datetime


class SolicitudesService:
    def __init__(self, repo):
        self.repo = repo

    ## S2 - LONG METHOD (función extensa, realiza múltiples tareas)
    ## S3 - LONG PARAMETER LIST (demasiados parámetros)
    def registrar(self, nombre, apellido, dni, email, legajo, carrera, tipo, prioridad, detalle, resp):

        if nombre == None or nombre == "": ## S10 - CONDICIONALES EXTENSOS
            return "error nombre"
        if apellido == None or apellido == "":
            return "error apellido"
        if dni == None or len(str(dni)) < 7 or len(str(dni)) > 8:   ## S5 - MAGIC NUMBERS
            return "error dni"
        if email == None or "@" not in email:
            return "error email"
        if tipo != "certificado" and tipo != "equivalencia" and tipo != "reclamo":
            return "error tipo"
        if prioridad != "baja" and prioridad != "media" and prioridad != "alta":
            return "error prioridad"
        if detalle == None or len(detalle) < 10:     ## S5 - MAGIC NUMBERS
            return "error detalle"
        est_id = 0
        for e in self.repo.estudiantes:
            if e["dni"] == str(dni):
                est_id = e["id"]
        if est_id == 0:
            self.repo.cont_est = self.repo.cont_est + 1
            self.repo.estudiantes.append({"id": self.repo.cont_est, "nombre": nombre, "apellido": apellido, "dni": str(dni), "email": email, "legajo": legajo, "carrera": carrera})
            est_id = self.repo.cont_est
        if tipo == "certificado":      ## S5 - MAGIC NUMBERS & S10 - CONDICIONALES EXTENSOS
            plazo = 5
        elif tipo == "equivalencia":
            plazo = 30
        elif tipo == "reclamo":
            plazo = 10
        else:
            plazo = 15
        if prioridad == "alta":
            plazo = plazo // 2
        elif prioridad == "baja":
            plazo = plazo + 5
        hoy = datetime.datetime.now()
        venc = hoy + datetime.timedelta(days=plazo)
        self.repo.cont = self.repo.cont + 1
        nombre_resp = ""
        id_resp = 0
        if resp != None and resp != 0:
            for r in self.repo.responsables:
                if r["id"] == resp:
                    nombre_resp = r["nombre"]
                    id_resp = r["id"]
        s = {                              ## S8 - PRIMITIVE OBSESSION (Uso masivo de diccionarios planos)
            "id": self.repo.cont,
            "estudiante_id": est_id,
            "nombre": nombre,
            "apellido": apellido,
            "dni": str(dni),
            "email": email,
            "legajo": legajo,
            "carrera": carrera,
            "tipo": tipo,
            "prioridad": prioridad,
            "estado": "pendiente",
            "detalle": detalle,
            "responsable_id": id_resp,
            "responsable": nombre_resp,
            "fecha": hoy.strftime("%d/%m/%Y"),
            "vencimiento": venc.strftime("%d/%m/%Y"),
            "historial": ["pendiente " + hoy.strftime("%d/%m/%Y %H:%M")],
        }
        self.repo.solicitudes.append(s)
        self.repo.guardar()
        print("solicitud registrada " + str(self.repo.cont))  ## S13 - PRINT COMO LOG Y CÓDIGO MUERTO/MENSAJES EN CONSOLA
        return s  ## S11 - TIPO DE RETORNO INCONSISTENTE (devuelve dict o str)

    ## S2 - LONG METHOD (función extensa, realiza múltiples tareas)
    def cambiar_estado(self, id, estado):
        for s in self.repo.solicitudes:
            if s["id"] == id:
                if estado != "pendiente" and estado != "en proceso" and estado != "resuelta":
                    return "error estado"
                if s["estado"] == "resuelta":
                    return "error ya resuelta"
                if s["estado"] == "pendiente":
                    if estado == "en proceso" or estado == "resuelta":
                        if estado == "en proceso" and s["responsable_id"] == 0:
                            return "error sin responsable"
                        s["estado"] = estado
                    else:
                        return "error transicion"
                elif s["estado"] == "en proceso":
                    if estado == "resuelta":
                        s["estado"] = estado
                    else:
                        return "error transicion"
                s["historial"].append(estado + " " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
                self.repo.guardar()
                return s
        return None

    def asignar(self, id, resp):
        for s in self.repo.solicitudes:
            if s["id"] == id:
                for r in self.repo.responsables:
                    if r["id"] == resp:
                        s["responsable_id"] = r["id"]
                        s["responsable"] = r["nombre"]
                        s["historial"].append("asignada a " + r["nombre"] + " " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
                        self.repo.guardar()
                        return s
                return "error responsable"
        return None

    def listar(self, estado, tipo, prioridad, dni):   ## S6 - CÓDIGO DUPLICADO (Filtros repetidos)
        res = []
        for s in self.repo.solicitudes:
            ok = True
            if estado != None and estado != "":    
                if s["estado"] != estado:
                    ok = False
            if tipo != None and tipo != "":
                if s["tipo"] != tipo:
                    ok = False
            if prioridad != None and prioridad != "":
                if s["prioridad"] != prioridad:
                    ok = False
            if dni != None and dni != "":
                if s["dni"] != dni:
                    ok = False
            if ok:
                res.append(s)
        return res

    def reporte(self):
        p = 0         ## S12 - NOMBRES POCO DESCRIPTIVOS (Variables de una sola letra)
        e = 0
        r = 0
        for s in self.repo.solicitudes:
            if s["estado"] == "pendiente":
                p = p + 1
            if s["estado"] == "en proceso":
                e = e + 1
            if s["estado"] == "resuelta":
                r = r + 1
        t = len(self.repo.solicitudes)
        if t == 0:
            return {"total": 0, "pendiente": 0, "en proceso": 0, "resuelta": 0, "porc_resueltas": 0}
        alta = 0
        for s in self.repo.solicitudes:
            if s["prioridad"] == "alta" and s["estado"] != "resuelta":
                alta = alta + 1
        print("reporte generado")
        return {"total": t, "pendiente": p, "en proceso": e, "resuelta": r, "porc_resueltas": round(r * 100 / t, 2), "alta_sin_resolver": alta}
