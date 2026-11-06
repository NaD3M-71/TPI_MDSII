import os
import sys

from fastapi.testclient import TestClient

# Esto le dice a Python que agregue la raíz del proyecto al buscador de módulos, ya que la arquitectura inicial no contiene a main.py dentro de un paquete. Esto permite importar main.py desde tests/test_main.py sin problemas.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_leer_responsables():
    """Verifica el endpoint GET /responsables"""
    response = client.get("/responsables")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_crear_solicitud_valida():
    """Verifica la creación exitosa de una solicitud (POST /solicitudes)"""
    payload = {
        "nombre": "Ana",
        "apellido": "Perez",
        "dni": "38440237",
        "email": "ana.perez@utn.edu.ar",
        "legajo": "12345",
        "carrera": "TUP",
        "tipo": "certificado",
        "prioridad": "alta",
        "detalle": "Necesito certificado de alumno regular actualizado.",
        "responsable_id": 1
    }
    response = client.post("/solicitudes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "solicitud" in data
    assert data["solicitud"]["nombre"] == "Ana"

def test_listar_solicitudes():
    """Verifica la consulta general de solicitudes (GET /solicitudes)"""
    response = client.get("/solicitudes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_filtrar_solicitudes_por_dni():
    """Verifica el filtrado por query param (GET /solicitudes?dni=...)"""
    response = client.get("/solicitudes?dni=38440237")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert data[0]["dni"] == "38440237"

def test_ver_solicitud_por_id():
    """Verifica la búsqueda de una solicitud específica (GET /solicitudes/{id})"""
    # Asumimos que al menos el ID 1 existe por la prueba anterior
    response = client.get("/solicitudes/1")
    # Si existe debe retornar 200, si no 404
    assert response.status_code in [200, 404]

def test_obtener_reporte():
    """Verifica la generación de métricas (GET /reporte)"""
    response = client.get("/reporte")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    
def test_crear_solicitud_tipo_invalido():
    """
    Caracteriza el manejo de errores inicial: ante un tipo de trámite inválido.
    - Qué testea: Demuestra el manejo de errores deficiente actual. Ante un tipo de 
      trámite inválido ('analitico'), el sistema responde con HTTP 200 OK (incorrecto 
      para un error de validación) y un mensaje de texto plano en el JSON ('ok': false).
    - Por qué fallará después el refactor: Al corregir el diseño y aplicar excepciones de dominio,
      el sistema deberá rechazar la petición con un código HTTP estándar (como 400 Bad Request 
      o 422 Unprocessable Entity). Cuando eso ocurra, esta prueba fallará a propósito, 
      exigiéndonos actualizarla para reflejar la mejora en la calidad interna.
    """
    """
    Verifica que el sistema rechace un tipo de trámite inválido 
    con un código HTTP semántico (422 Unprocessable Entity por validación de Enum en Pydantic).
    """
    payload = {
        "nombre": "Laura",
        "apellido": "Ramirez",
        "dni": "42551335",
        "email": "laura_r@utn.edu.ar",
        "legajo": "67890",
        "carrera": "TUP",
        "tipo": "analitico",  # Tipo no contemplado originalmente
        "prioridad": "alta",
        "detalle": "Necesito analitico por haber finalizado mis estudios.",
        "responsable_id": 2
    }
    response = client.post("/solicitudes", json=payload)
    
    # Afirmamos el comportamiento actual (aunque conceptualmente sea una mala práctica)
    #modificacion Actualizado: Esperamos 422 por validación estricta de Pydantic (agus)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # Pydantic devuelve detalles de validación en 'detail'
    ##assert data["ok"] is False
    ##assert "error tipo" in data["msg"]


def test_crear_solicitud_prioridad_invalida():
    """
    Caracteriza el manejo de errores inicial ante una prioridad inválida.
    - Qué testea: Comportamiento inicial ante una prioridad inválida ('medio'). 
      Devuelve HTTP 200 OK con un mensaje plano de error.
    - Por qué fallará después el refactor: Al igual que el test anterior, se espera que 
      el sistema devuelva un código HTTP de error semántico (400/422). Esta prueba 
      actuará como disparador para comprobar que mejoramos el manejo de excepciones.
    """
    """
    Verifica que el sistema rechace una prioridad inválida 
    con un código HTTP semántico (422 Unprocessable Entity por validación de Enum en Pydantic).
    """
    payload = {
        "nombre": "Laura",
        "apellido": "Ramirez",
        "dni": "42551335",
        "email": "laura_r@utn.edu.ar",
        "legajo": "67890",
        "carrera": "TUP",
        "tipo": "certificado",
        "prioridad": "medio",  # Prioridad incorrecta (debería ser alta/baja/normal)
        "detalle": "Prueba de prioridad inválida",
        "responsable_id": 2
    }
    response = client.post("/solicitudes", json=payload)
    # modificacion Actualizado: Esperamos 422 por validación estricta de Pydantic (agustin)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # Pydantic devuelve detalles de validación en 'detail'
    ##assert data["ok"] is False
    ##assert "error prioridad" in data["msg"]
    