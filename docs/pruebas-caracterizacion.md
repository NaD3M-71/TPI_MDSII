## Etapa de Pruebas de Caracterización (Commit C2)

Se implementó una suite de pruebas automatizadas utilizando **Pytest** y el cliente de pruebas de **FastAPI** (`TestClient`), ubicada en el directorio `tests/test_main.py`.

### Propósito
Congelar y documentar el comportamiento inicial del sistema (incluyendo las debilidades y la deuda técnica identificada en el diagnóstico), sirviendo como una red de seguridad indispensable para validar que las futuras refactorizaciones no rompan la funcionalidad existente.

### Ejecución de la Suite
Para correr las pruebas en el entorno local, ejecutar los siguientes comandos en la terminal:

```bash
# 1. Activar el entorno virtual
.venv\Scripts\Activate

# 2. Ejecutar la suite de pruebas en modo verboso
pytest -v