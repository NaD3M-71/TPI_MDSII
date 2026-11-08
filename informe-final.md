# Informe Técnico de Validación y Cierre (TPI MDS II)

## Resumen Ejecutivo
Este informe documenta la culminación de la fase de validación, pruebas de regresión y refactorización del Trabajo Práctico Integrador (TPI) de la materia Metodología de Sistemas II (UTN). El sistema consiste en una API desarrollada en **FastAPI** bajo una arquitectura limpia y modularizada (`repositories`, `services`, `routes`, `schemas` y `core`). 

El objetivo principal de este hito fue blindar el sistema mediante una suite de pruebas robusta con **`pytest`** y **`pytest-cov`**, alcanzando un nivel de cobertura del **87%** y garantizando la estabilidad operativa del software frente a futuros cambios.

---

## Diagnóstico Inicial y Estado Previo del Sistema
En las etapas iniciales del TPI, el sistema presentaba diversos desafíos arquitectónicos y de mantenibilidad que requerían intervención:
* **Acoplamiento Fuerte:** La lógica de negocio y el acceso a datos se encontraban fuertemente entrelazados, dificultando la prueba aislada de los componentes.
* **Manejo de Errores Deficiente:** Bloques `try-except` vacíos (silenciosos) que ocultaban excepciones de lectura/escritura en archivos o fallos de negocio.
* **Duplicación de Código y Complejidad Ciclomática:** Funciones extensas con múltiples anidamientos de condiciones `if/else` para el control de estados y filtros de búsqueda.
* **Ausencia de Pruebas Automatizadas:** Cobertura inicial nula o extremadamente baja, lo que impedía validar de forma segura refactorizaciones o evoluciones del código.

---

## Pruebas de Caracterización y Estrategia de Testing
Para mitigar el riesgo de romper la funcionalidad existente durante la refactorización, se implementó una estrategia basada en **pruebas de caracterización** e integración:

1. **Línea Base de Comportamiento:** Se diseñaron inicialmente pruebas de integración básicas usando `TestClient` de FastAPI para capturar el comportamiento observable de los endpoints críticos (`/solicitudes`, `/reporte`, `/responsables`).
2. **Expansión y Casos de Borde:** La suite de pruebas creció progresivamente hasta alcanzar **17 casos de prueba** automatizados que cubren:
   - Caminos felices (creación, listado, filtros combinados y cambios de estado válidos).
   - Manejo de excepciones y validaciones de negocio (códigos HTTP 400, 404 y 422).
   - Transiciones de estado inválidas y asignación de responsables inexistentes.
   - Robustez ante errores de decodificación en repositorios de persistencia basados en archivos JSON.

---

## Evolución de la Cobertura de Código
Gracias a la incorporación iterativa de pruebas unitarias y de integración, la cobertura de código evolucionó de manera sostenida hasta alcanzar los siguientes valores finales validados mediante `pytest-cov`:

| Módulo / Archivo | Cobertura Final | Estado |
| :--- | :---: | :---: |
| `core/dependencies.py` | **100%** | Óptimo |
| `models/enums.py` | **100%** | Óptimo |
| `schemas/solicitudes.py` | **100%** | Óptimo |
| `services/calculadora_plazos.py` | **100%** | Óptimo |
| `repositories/solicitudes_repository.py` | **93%** | Robusto |
| `tests/test_main.py` | **98%** | Excelente |
| `routes/reportes.py` / `responsables.py` | **80%** | Sólido |
| `services/solicitudes_service.py` | **72%** | Aceptable (Lógica central cubierta) |
| `routes/solicitudes.py` | **71%** | Sólido |
| **TOTAL GENERAL DEL SISTEMA** | **87%** | **Objetivo Cumplido (Exitoso)** |

---

## Conclusiones y Próximos Pasos (Tag v1.0)
La implementación de principios SOLID, inyección de dependencias y una suite de 17 pruebas automatizadas que corren en verde de forma consistente (`17 passed in ~5-14s`) garantiza que la aplicación se encuentra en condiciones óptimas de entrega. 
