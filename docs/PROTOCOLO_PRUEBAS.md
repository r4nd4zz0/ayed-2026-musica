# Protocolo de regresión

Pruebas manuales para ejecutar desde la raíz con `python -m src.main`. Registrar el resultado observado en la columna Resultado; no marcar un caso como aprobado sin ejecutar sus pasos sobre el estado final que se entrega.

Leyenda: `Pasa`, `No pasa` o `No corrido`.

**Estado de esta revisión:** los casos están especificados, pero no se ejecutaron desde este entorno; por eso quedan `No corrido`. Antes de crear el tag `entrega-6`, el equipo debe ejecutarlos, anotar el resultado real y completar notas si aparece una diferencia.

| ID | Entrega | Acción (pasos en el CLI) | Datos | Resultado esperado | Resultado | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | E1 | Iniciar y elegir listar catálogo (1). | Dataset original. | Se muestra un catálogo no vacío, sin traceback. | No corrido | |
| P02 | E1 | Ver detalle (2) de un ID inexistente. | ID `-1`. | Informa que no existe y vuelve al menú. | No corrido | |
| P03 | E1 | Ver detalle (2) con entrada no numérica. | `abc`. | Informa que el ID debe ser entero y vuelve al menú. | No corrido | |
| P04 | E1 | Buscar (3), elegir lineal (1), buscar un título existente. | `De Musica Ligera`. | Se encuentra la canción. | No corrido | |
| P05 | E1 | Buscar (3), elegir lineal (1), ingresar un título inexistente. | `zzzz`. | Informa que no se encontró. | No corrido | |
| P06 | E2 | Operación recursiva (5) para una canción con derivada. | ID `1`. | Se muestra la canción base y su versión derivada ID 62. | No corrido | |
| P07 | E2 | Operación recursiva (5) para una hoja. | ID `62`. | Informa que no tiene versiones derivadas. | No corrido | |
| P08 | E2 | Operación recursiva (5) para ID inexistente. | ID `9999`. | Informa que no existe el ID y el programa sigue. | No corrido | |
| P09 | E3 | En colección principal (6), agregar dos elementos (1) y listarlos (2). | Dos textos distintos. | El iterador los muestra en el orden de inserción. | No corrido | |
| P10 | E3 | En historial (7), desapilar (3) con pila vacía. | Pila recién iniciada. | Muestra el error de pila vacía y permite continuar. | No corrido | |
| P11 | E3 | En cola (8), desencolar (3) con cola vacía. | Cola recién iniciada. | Muestra el error de cola vacía y permite continuar. | No corrido | |
| P12 | E3 | En historial (7), apilar (1), consultar tope (2) y desapilar (3). | Acción `prueba`. | El tope y el elemento desapilado son `prueba`. | No corrido | |
| P13 | E4 | Intentar búsqueda binaria (3, opción 2) antes de ordenar; luego ordenar por título (4) y buscar. | Título existente. | Antes de ordenar avisa; después encuentra el título. | No corrido | |
| P14 | E4 | Ordenar (4) usando selección e inserción; probar ambos criterios. | Dataset completo. | El orden resultante corresponde al criterio y no hay errores. | No corrido | |
| P15 | E5 | Guardar texto y binario (9); modificar un registro mediante ABM; reiniciar y cargar texto; probar archivo inválido. | Catálogo original y copia de prueba corrupta. | El cambio persiste al recargar; la carga corrupta muestra error controlado, sin traceback. | No corrido | No subir el `.bin` de prueba. |

