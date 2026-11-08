# TPI - Metodología de Sistemas II

Trabajo Práctico Integrador enfocado en la evolución profesional de un sistema existente, priorizando la mejora de la calidad interna, la reducción de deuda técnica y la aplicación de principios SOLID y Clean Code.

## Integrantes del Equipo
- Rivarola, Agustín
- Rivarola, Esteban
- Romero, Daniela
- Scaglioni, Giuliano

## Sistema base

El sistema es una API monolítica desarrollada en FastAPI que gestiona solicitudes académicas (certificados, equivalencias y reclamos). Permite registrar estudiantes, asignar responsables, cambiar estados mediante un flujo definido y generar reportes estadísticos básicos.

## Tecnologías utilizadas
- **Python 3.10+**
- **FastAPI** (Framework web)
- **Uvicorn** (Servidor ASGI)

## Instalación y ejecución

1. Clonar el repositorio y posicionarse en la rama/tag inicial:
   ```bash
   git checkout estado-inicial
   ```
2. Crear un entorno virtual de Python:
   ```bash
   python -m venv .venv
   ```
3. Activar el entorno virtual:
   ```bash
   .venv\Scripts\Activate.ps1
   ```
4. Instalar todas las librerías y dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. Iniciar el servidor de desarrollo de FastAPI utilizando el archivo principal de la aplicación (main.py):
   ```bash
   python -m fastapi dev main.py
   ```

## Ejecución de Pruebas (Tests)

   Para correr la suite completa de pruebas unitarias y de integración con `pytest`, ejecuta el siguiente comando en la raíz del proyecto:

   ```bash
   pytest -v --cov=.
   ```