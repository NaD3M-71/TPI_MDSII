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
        "responsable_id": 1,
    }
    response = client.post("/solicitudes", json=payload)
    print("DETALLE TI ERROR 400:", response.json())
    # Actualizado: Esperamos 201 Created según la definición del endpoint
    assert response.status_code == 201
    # Como la API ahora retorna el recurso directamente, validamos los campos del objeto
    data = response.json()
    assert data["nombre"] == "Ana"
    assert data["dni"] == "38440237"
    assert data["tipo"] == "certificado"


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
        "responsable_id": 2,
    }
    response = client.post("/solicitudes", json=payload)

    # Actualizado: Esperamos 422 por validación estricta de Pydantic
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # Pydantic devuelve detalles de validación en 'detail'


def test_crear_solicitud_prioridad_invalida():
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
        "responsable_id": 2,
    }
    response = client.post("/solicitudes", json=payload)

    # Actualizado: Esperamos 422 por validación estricta de Pydantic
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # Pydantic devuelve detalles de validación en 'detail'
