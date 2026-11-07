# Documentación de Arquitectura y Refactorización

Este documento registra los cambios estructurales aplicados para desacoplar la aplicación monolítica inicial hacia una arquitectura en capas mantenible y testend-driven.

## Estado Actual del Sistema: Desacoplamiento Final, Inyección de Dependencias y Calidad de Código

1. **Estructura en Capas:**
   - `schemas/`: DTOs de validación con Pydantic y Enums estrictos (`TipoSolicitud`, `Prioridad`).
   - `services/`: Lógica de negocio desacoplada de los frameworks HTTP.
   - `repositories/`: Capa de persistencia y acceso a datos.
   - `routes/`: Endpoints limpios de FastAPI que manejan contratos HTTP estándar.

2. **Manejo de Errores y Excepciones:**
   - Validación automática de entradas mediante Pydantic (respuestas HTTP `422 Unprocessable Entity`).
   - Control de reglas de negocio mediante excepciones controladas (`HTTP 400 Bad Request`).
   - Eliminación gradual de bloques `except:` genéricos en favor de excepciones semánticas.

3. **Calidad de Código y Testing:**
   - Suite de pruebas automatizada con `pytest` que verifica tanto flujos felices (`201 Created`, `200 OK`) como validaciones estrictas.
   - Cobertura del 100% en verde sobre los tests de caracterización e integración.

4. **Inyección de Dependencias:** 
   Se centralizó la creación de servicios y repositorios mediante un módulo de configuración (`dependencies.py` / *Composition Root*), evitando que las capas de presentación (routers) instancien directamente la persistencia.

5. **Nomenclatura Clara y Transparente:** 
   Se eliminaron las variables abreviadas crípticas (`ARCH`, `cont`, `d`, `f`) por nombres semánticos y autoexplicativos (`ARCHIVO_DATOS`, `contador_solicitudes`, `contenido_json`, etc.).

6. **Principio de Responsabilidad Única (SRP) y OCP:** 
   Consolidación de la `CalculadoraPlazos` y tablas de transición inmutables en los servicios.

### Validación de Calidad

* **Automatización:** Ejecución exitosa de la suite de pruebas automatizadas con `pytest` (todos los tests en verde).
* **Estándares PEP 8:** Verificación activa mediante ganchos de `pre-commit` y formateo con Ruff.