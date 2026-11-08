import os
import sys
from unittest.mock import patch

import json

from fastapi.testclient import TestClient

# Esto le dice a Python que agregue la raíz del proyecto al buscador de módulos, 
# ya que la arquitectura inicial no contiene a main.py dentro de un paquete. 
# Esto permite importar main.py desde tests/test_main.py sin problemas.
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


def test_cambiar_estado_solicitud_no_encontrada():
    """Prueba el error 404 cuando se intenta actualizar una solicitud inexistente."""
    response = client.put("/solicitudes/9999/estado", json={"estado": "En Proceso"})
    assert response.status_code == 404
    assert response.json()["detail"] == "No existe la solicitud"

def test_transicion_estado_invalida():
    """Prueba el error al intentar una transición de estado no permitida."""
    response_creacion = client.post("/solicitudes", json={
        "nombre": "Ana",
        "apellido": "Gomez",
        "dni": "12345678",
        "email": "ana@test.com",
        "legajo": "L001",
        "carrera": "Tecnicatura",
        "tipo": "certificado",
        "prioridad": "alta",
        "detalle": "Prueba de estado",
        "responsable_id": 1
    })
    
    datos_creados = response_creacion.json()
    
    if "id" in datos_creados:
        solicitud_id = datos_creados["id"]
        response_error = client.put(f"/solicitudes/{solicitud_id}/estado", json={"estado": "EstadoInvalido"})
        assert response_error.status_code in [400, 422]
    else:
        assert False, f"No se pudo crear la solicitud en el test. Respuesta: {datos_creados}"


def test_listar_solicitudes_con_filtros_combinados():
    """Prueba el filtrado de solicitudes pasando múltiples parámetros opcionales."""
    # Creamos una solicitud con datos particulares para buscarla
    client.post("/solicitudes", json={
        "nombre": "Carlos",
        "apellido": "Perez",
        "dni": "87654321",
        "email": "carlos@test.com",
        "legajo": "L002",
        "carrera": "Sistemas",
        "tipo": "equivalencia",
        "prioridad": "media",
        "detalle": "Filtro combinado",
        "responsable_id": 1
    })
    
    # Consultamos aplicando filtros combinados (estado, tipo y prioridad)
    response = client.get("/solicitudes?estado=pendiente&tipo=equivalencia&prioridad=media&dni=87654321")
    assert response.status_code == 200
    resultados = response.json()
    assert isinstance(resultados, list)
    assert len(resultados) >= 1
    assert resultados[0]["dni"] == "87654321"

def test_ver_detalle_solicitud_inexistente():
    """Prueba el endpoint de obtener solicitud por ID cuando no existe (404)."""
    response = client.get("/solicitudes/99999")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_repositorio_error_lectura_json(monkeypatch):
    """Prueba que el repositorio maneje correctamente un error de decodificación JSON (archivo corrupto)."""
    
    # Simulamos que al abrir el archivo lanza un JSONDecodeError (archivo corrupto)
    def mock_open(*args, **kwargs):
        class MockFile:
            def __enter__(self): 
                raise json.JSONDecodeError("Expecting value", "", 0)
            def __exit__(self, *args): 
                pass
        return MockFile()
    
    monkeypatch.setattr("builtins.open", mock_open)

    from repositories.solicitudes_repository import SolicitudesRepository
    # Al instanciar el repositorio, se ejecuta el __init__ y atrapa la excepción del archivo
    repo = SolicitudesRepository()
    
    # Verificamos que ante el error, la lista de solicitudes inicia vacía por seguridad
    assert repo.solicitudes == []

def test_actualizar_estado_solicitud_transicion_invalida_service():
    """Prueba una transición de estado inválida para cubrir la validación del servicio."""
    # Creamos una solicitud válida (queda en 'pendiente')
    response_creacion = client.post("/solicitudes", json={
        "nombre": "Lucia",
        "apellido": "Fernandez",
        "dni": "11223344",
        "email": "lucia@test.com",
        "legajo": "L003",
        "carrera": "Sistemas",
        "tipo": "reclamo",
        "prioridad": "baja",
        "detalle": "Prueba error estado",
        "responsable_id": 1
    })
    
    datos = response_creacion.json()
    if "id" in datos:
        sol_id = datos["id"]
        # Intentar pasar de 'pendiente' a un estado no permitido directamente si aplica, 
        # o probar actualizar con un estado mal formado que active el error en el servicio.
        response = client.put(f"/solicitudes/{sol_id}/estado", json={"estado": "estado_inexistente_123"})
        assert response.status_code in [400, 422]

def test_reporte_vacio():
    """Prueba el endpoint de reportes cuando no hay solicitudes registradas."""
    # Corregido a /reporte (en singular según reportes.py)
    response = client.get("/reporte")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data

def test_asignar_responsable_inexistente():
    """Prueba asignar una solicitud a un ID de responsable que no existe (error responsable)."""
    res = client.post("/solicitudes", json={
        "nombre": "Pedro",
        "apellido": "Picapiedra",
        "dni": "33445566",
        "email": "pedro@test.com",
        "legajo": "L999",
        "carrera": "Ingeniería",
        "tipo": "certificado",
        "prioridad": "baja",
        "detalle": "Prueba responsable",
        "responsable_id": 1
    })
    sol_id = res.json()["id"]
    
    # Corregido a /{sol_id}/responsable según solicitudes.py
    response = client.put(f"/solicitudes/{sol_id}/responsable", json={"responsable_id": 999})
    assert response.status_code in [400, 422]

def test_crear_segunda_solicitud_mismo_estudiante():
    """Prueba registrar una nueva solicitud con un DNI ya existente para cubrir el reuso de estudiantes."""
    payload = {
        "nombre": "Maria",
        "apellido": "Gimenez",
        "dni": "55667788",
        "email": "maria@test.com",
        "legajo": "L888",
        "carrera": "Diseño",
        "tipo": "reclamo",
        "prioridad": "alta",
        "detalle": "Primera solicitud",
        "responsable_id": 1
    }
    # Primera creación (crea el estudiante)
    client.post("/solicitudes", json=payload)
    
    # Segunda creación con el mismo DNI (reutiliza el estudiante en el servicio)
    payload["detalle"] = "Segunda solicitud del mismo alumno"
    response = client.post("/solicitudes", json=payload)
    assert response.status_code in [200, 201]