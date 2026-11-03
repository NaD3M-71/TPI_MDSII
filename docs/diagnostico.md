# Diagnóstico de Calidad y Deuda Técnica

En este documento se busca identificar de manera formal las debilidades estructurales y de diseño, asi como los code smells  que presenta el prototipo base del sistema. Aunque el código funciona ha acumulado mucha deuda técnica, lo que reduce drásticamente la mantenibilidad del software, dificulta futuras ampliaciones y vuelve al sistema frágil frente a cualquier cambio. Este análisis nos servirá como mapa de ruta para las refactorizaciones a realizar para que el c´pfigo logre esta basado en los principios SOLID y Clean Code.

## Calidad externa vs. calidad interna

- **Calidad Externa (aceptable):** Es importante mencionar que, desde la perspectiva del usuario, el sistema cumple con las operaciones funcionales exigidas (crear, listar, cambiar estado y reportar) y los endpoints funcionan. Esto ultimo fue probado y verificado mediante la interfaz interactiva de Swagger (/docs). Lo cual se evidenciara en el modulo de pruebas a crear en el prpoximo sprint que nos serviran de base para registrar como funciona el sistema ahora en su etapa inicial y verificar no haber modificado su comportamiento despues del refactoring.

- **Calidad Interna (deficiente):**  nivel interno y estructural, el código presenta una alta deuda técnica. Todo el modelo de negocio, las validaciones, el manejo de archivos y las rutas están acoplados en un único archivo (`main.py`) y en una clase monolítica (`Gestor`), lo que impide la mantenibilidad y la escalabilidad.

## Code Smells
A continuación se detallan los *code smells* (13) identificados en el estado inicial (`main.py`):

#### S1 - God Class (Clase Monolítica)
- **Ubicación:** Clase `Gestor` (líneas 22-202).
- **Qué significa:** Una sola clase asume demasiadas responsabilidades al mismo tiempo. En este caso, la clase se encarga de leer y guardar archivos, validar datos, calcular plazos de entrega, armar los diccionarios de solicitudes, cambiar estados, filtrar listados y generar reportes estadísticos. Cualquier cambio mínimo en una regla de negocio obliga a modificar esta misma clase, volviendo imposible probar una parte del sistema de forma aislada.

#### S2 - Estado Global Mutable
- **Ubicación:** Líneas 10-18 y uso de la sentencia `global` en las líneas 24 y 51.
- **Qué significa:** Las listas de solicitudes, estudiantes y los contadores de IDs viven sueltas a nivel general del módulo y son modificadas directamente desde las funciones utilizando la palabra reservada `global`. Esto genera dependencias ocultas y hace que el comportamiento del sistema dependa estrictamente del orden en que se ejecuten las funciones, lo que podría generar inconsistencias si hay múltiples peticiones simultáneas.

#### S3 - Long Method (Métodos Demasiado Largos)
- **Ubicación:** Funciones `registrar` (líneas 48-119) y `cambiar_estado` (líneas 121-149).
- **Qué significa:** Funciones que realizan múltiples tareas complejas en un solo bloque y acumulan demasiados niveles de condiciones anidadas (`if/else`). Son muy difíciles de leer, de entender y de mantener.

#### S4 - Long Parameter List / Data Clumps (Exceso de Parámetros)
- **Ubicación:** Función `registrar` (línea 48) y `listar` (línea 172).
- **Qué significa:** Funciones que reciben una lista interminable de argumentos sueltos (como nombre, apellido, DNI, email, legajo y carrera por separado) en lugar de agruparlos lógicamente en un objeto o estructura. Es muy fácil equivocarse en el orden al pasar los argumentos, y cualquier dato nuevo obliga a modificar la firma de múltiples funciones.

#### S5 - Magic Numbers y Magic Strings (Números y Textos Mágicos)
- **Ubicación:** Líneas 58, 66, 75-84, 111, 116 y los estados literales en todo el archivo.
- **Qué significa:** Uso de valores fijos repartidos por el código sin un nombre explicativo (por ejemplo, plazos numéricos como 5, 30, 10 o strings sueltos como `"pendiente"`, `"en proceso"`). Si una regla de negocio cambiara, hay que buscar manualmente dónde quedó escrito ese número. Un simple error de tipeo en un string de texto pasa inadvertido y rompe la lógica.

#### S6 - Código Duplicado
- **Ubicación:** Líneas 175-188 (filtros de listados) y bloques repetidos en conteos de reportes y búsquedas.
- **Qué significa:** Escribir la misma lógica o bloques de código similares en varios lugares distintos en lugar de reutilizarlos. Si se detecta un error o se actualiza una regla, hay que acordarse de modificarla en todos los lugares donde fue duplicada, lo que lleva fácilmente a olvidos e inconsistencias.

#### S7 - Manejo de Errores Deficiente
- **Ubicación:** Líneas 35-36, 42-43, 219-220, 251-252 y 265-266 (bloques `except:` vacíos o genéricos).
- **Qué significa:** Capturar errores generales sin especificar qué tipo de excepción ocurrió y utilizar un `pass` para silenciar el fallo, devolviendo además códigos HTTP incorrectos (como responder con un código `200 OK` cuando en realidad ocurrió un error). Si ocurre un fallo al guardar los datos, el sistema lo oculta y la información se pierde sin dejar rastro.

#### S8 - Primitive Obsession (Obsesión por los Tipos Primitivos)
- **Ubicación:** Todo el archivo (bloque de construcción del diccionario de solicitud en líneas 97-115).
- **Qué significa:** Utilizar únicamente diccionarios genéricos y cadenas de texto primitivas para modelar entidades complejas del dominio en lugar de clases o estructuras tipadas. Las claves de los diccionarios pueden escribirse mal y el error solo se descubre en tiempo de ejecución.

#### S9 - Acoplamiento Fuerte
- **Ubicación:** Instanciación directa de `Gestor()` dentro de cada endpoint web (líneas 213, 225, 232, 245, 260, etc.).
- **Qué significa:** Las rutas web y la lógica de negocio están fuertemente atadas a implementaciones concretas. Impide reutilizar componentes, dificulta la escritura de pruebas automatizadas y hace imposible cambiar la persistencia sin romper el código.

#### S10 - Condicionales Extensos
- **Ubicación:** Líneas 53-56, 75-84 y 125-144 (validaciones de entrada y cálculo de plazos o estados).
- **Qué significa:** Uso excesivo de estructuras condicionales complejas para tomar decisiones basadas en tipos o estados. Agregar un nuevo tipo de solicitud o un nuevo estado en el futuro obliga a modificar directamente la estructura de los condicionales existentes, violando el principio OCP.

#### S11 - Tipos de Retorno Inconsistentes
- **Ubicación:** Funciones `registrar`, `cambiar_estado` y `asignar`.
- **Qué significa:** Funciones que según el caso pueden devolver un diccionario con datos, un texto plano indicando un error, o un valor nulo (`None`). Quien consume estas funciones se ve obligado a evaluar constantemente de qué tipo es la respuesta mediante condiciones confusas.

#### S12 - Nombres Poco Descriptivos
- **Ubicación:** Variables de una sola letra `p`, `e`, `r` (líneas 193-195) y nombres de funciones abreviados `resps` (línea 270), `rep` (línea 275).
- **Qué significa:** Uso de identificadores que no comunican claramente qué representan o qué hacen, obligando al lector a recorrer todo el bloque de código para deducir su propósito.

#### S13 - Código Muerto y Uso de Prints como Logs
- **Ubicación:** Líneas 117, 206 (`print`) y línea 232 (`g = Gestor()` instanciado pero no utilizado en el endpoint `ver`).
- **Qué significa:** Presencia de código que nunca se ejecuta y uso de consola (`print`) en lugar de un sistema de registro profesional (`logging`). Genera ruido visual y no aporta trazabilidad en producción.