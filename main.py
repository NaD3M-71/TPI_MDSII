import json
import os
import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

ARCH = "datos.json"
solicitudes = []
estudiantes = []
responsables = [
    {"id": 1, "nombre": "Laura Gomez", "area": "Alumnado"},
    {"id": 2, "nombre": "Carlos Perez", "area": "Titulos"},
    {"id": 3, "nombre": "Marta Diaz", "area": "Bedelia"},
]
cont = 0
cont_est = 0


class Gestor:
    def __init__(self):
        global solicitudes, estudiantes, cont, cont_est
        if os.path.exists(ARCH):
            try:
                f = open(ARCH, "r")
                d = json.loads(f.read())
                solicitudes = d["solicitudes"]
                estudiantes = d["estudiantes"]
                cont = d["cont"]
                cont_est = d["cont_est"]
            except:
                pass

    def guardar(self):
        try:
            f = open(ARCH, "w")
            f.write(json.dumps({"solicitudes": solicitudes, "estudiantes": estudiantes, "cont": cont, "cont_est": cont_est}))
        except:
            pass

    def registrar(self, nombre, apellido, dni, email, legajo, carrera, tipo, prioridad, detalle, resp):
        global cont, cont_est
        if nombre == None or nombre == "":
            return "error nombre"
        if apellido == None or apellido == "":
            return "error apellido"
        if dni == None or len(str(dni)) < 7 or len(str(dni)) > 8:
            return "error dni"
        if email == None or "@" not in email:
            return "error email"
        if tipo != "certificado" and tipo != "equivalencia" and tipo != "reclamo":
            return "error tipo"
        if prioridad != "baja" and prioridad != "media" and prioridad != "alta":
            return "error prioridad"
        if detalle == None or len(detalle) < 10:
            return "error detalle"
        est_id = 0
        for e in estudiantes:
            if e["dni"] == str(dni):
                est_id = e["id"]
        if est_id == 0:
            cont_est = cont_est + 1
            estudiantes.append({"id": cont_est, "nombre": nombre, "apellido": apellido, "dni": str(dni), "email": email, "legajo": legajo, "carrera": carrera})
            est_id = cont_est
        if tipo == "certificado":
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
        cont = cont + 1
        nombre_resp = ""
        id_resp = 0
        if resp != None and resp != 0:
            for r in responsables:
                if r["id"] == resp:
                    nombre_resp = r["nombre"]
                    id_resp = r["id"]
        s = {
            "id": cont,
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
        solicitudes.append(s)
        self.guardar()
        print("solicitud registrada " + str(cont))
        return s

    def cambiar_estado(self, id, estado):
        for s in solicitudes:
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
                self.guardar()
                return s
        return None

    def asignar(self, id, resp):
        for s in solicitudes:
            if s["id"] == id:
                for r in responsables:
                    if r["id"] == resp:
                        s["responsable_id"] = r["id"]
                        s["responsable"] = r["nombre"]
                        s["historial"].append("asignada a " + r["nombre"] + " " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
                        self.guardar()
                        return s
                return "error responsable"
        return None

    def listar(self, estado, tipo, prioridad, dni):
        res = []
        for s in solicitudes:
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
        p = 0
        e = 0
        r = 0
        for s in solicitudes:
            if s["estado"] == "pendiente":
                p = p + 1
            if s["estado"] == "en proceso":
                e = e + 1
            if s["estado"] == "resuelta":
                r = r + 1
        t = len(solicitudes)
        if t == 0:
            return {"total": 0, "pendiente": 0, "en proceso": 0, "resuelta": 0, "porc_resueltas": 0}
        alta = 0
        for s in solicitudes:
            if s["prioridad"] == "alta" and s["estado"] != "resuelta":
                alta = alta + 1
        print("reporte generado")
        return {"total": t, "pendiente": p, "en proceso": e, "resuelta": r, "porc_resueltas": round(r * 100 / t, 2), "alta_sin_resolver": alta}


@app.post("/solicitudes")
async def crear(request: Request):
    try:
        b = await request.json()
        g = Gestor()
        r = g.registrar(b.get("nombre"), b.get("apellido"), b.get("dni"), b.get("email"), b.get("legajo"), b.get("carrera"), b.get("tipo"), b.get("prioridad"), b.get("detalle"), b.get("responsable_id"))
        if type(r) == str:
            return {"ok": False, "msg": r}
        return {"ok": True, "solicitud": r}
    except Exception as e:
        return {"ok": False, "msg": "error"}


@app.get("/solicitudes")
def listar(estado: str = None, tipo: str = None, prioridad: str = None, dni: str = None):
    g = Gestor()
    return g.listar(estado, tipo, prioridad, dni)


@app.get("/solicitudes/{id}")
def ver(id: int):
    g = Gestor()
    for s in solicitudes:
        if s["id"] == id:
            return s
    return JSONResponse(status_code=404, content={"msg": "no existe"})


@app.put("/solicitudes/{id}/estado")
async def estado(id: int, request: Request):
    try:
        b = await request.json()
        g = Gestor()
        r = g.cambiar_estado(id, b["estado"])
        if r == None:
            return JSONResponse(status_code=404, content={"msg": "no existe"})
        if type(r) == str:
            return {"ok": False, "msg": r}
        return {"ok": True, "solicitud": r}
    except:
        return {"ok": False, "msg": "error"}


@app.put("/solicitudes/{id}/responsable")
async def responsable(id: int, request: Request):
    try:
        b = await request.json()
        g = Gestor()
        r = g.asignar(id, b["responsable_id"])
        if r == None:
            return JSONResponse(status_code=404, content={"msg": "no existe"})
        if type(r) == str:
            return {"ok": False, "msg": r}
        return {"ok": True, "solicitud": r}
    except:
        return {"ok": False, "msg": "error"}


@app.get("/responsables")
def resps():
    return responsables


@app.get("/reporte")
def rep():
    g = Gestor()
    return g.reporte()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
