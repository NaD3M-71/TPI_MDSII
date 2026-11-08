## Metodología de Trabajo y Flujo de Pull Requests

Para garantizar la estabilidad de la rama principal (`main`) y fomentar la colaboración transparente, el equipo adopta el siguiente flujo:

1. **Desarrollo en Ramas de Característica (Feature Branches):**
   - Ningún cambio se commitea directamente a `main`.
   - Cada refactor o historia de usuario se trabaja en una rama independiente (ej. `feature/refactor-modelos-esquemas`, `feature/refactor-excepciones`).

2. **Integración Continua Local:**
   - Antes de abrir o actualizar un PR, los integrantes deben integrar localmente las dependencias cruzadas y validar que la suite de pruebas corra sin errores (`pytest -v`).

3. **Code Review Colaborativo:**
   - Las revisiones se realizan mediante GitHub Pull Requests.
   - Se prioriza el feedback constructivo sobre contratos de API, códigos de estado HTTP y eliminación de *Code Smells*.

4. **Estrategia de Merge (Fusión):**
   - **Prohibido el uso de Squash and Merge** en las integraciones finales de refactor grupal.
   - Se utiliza estrictamente la opción **"Create a merge commit"** para asegurar que los commits individuales de cada autor queden reflejados en el historial de Git, visibilizando el esfuerzo compartido.