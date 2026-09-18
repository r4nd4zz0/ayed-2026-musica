# Protocolo de pruebas

Pruebas **manuales**. Cada fila es un caso. Ejecutar sobre el tag que entregan.

Leyenda de resultado: `pasa` / `no pasa` / `no corrido`.

Mínimos: 8 casos escritos en E2; ejecutados en E3; 15 de regresión en E6 (pila, cola, archivos, recursión, búsquedas).

| ID | Entrega | Acción (pasos en el CLI) | Datos | Resultado esperado | Resultado | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | E1 | Arrancar el programa y listar catálogo (opción 1) | dataset `canciones.csv` | Lista no vacía con formato `[id] título - artista`, sin traceback | pasa | Catálogo inicial cargado |
| P02 | E1 | Ver detalle con id inexistente (opción 2) | `id = -1` | Mensaje claro: "No existe la canción con id -1.", el menú continúa | pasa | Manejo de KeyError |
| P03 | E1 | Ver detalle con id no numérico (opción 2) | texto `abc` | Mensaje claro: "El id debe ser un número entero.", el menú continúa | pasa | Validación de entrada |
| P04 | E1 | Búsqueda por texto con coincidencia (opción 3) | texto existente en título | Lista todas las canciones coincidentes sin distinguir mayúsculas/minúsculas | pasa | Filtro por subcadena |
| P05 | E1 | Búsqueda por texto sin coincidencias (opción 3) | subcadena inexistente `zzzz` | Mensaje: "No se encontraron canciones con ese texto." | pasa | Búsqueda vacía |
| P06 | E2 | Operación recursiva sobre ítem con derivadas (opción 5) | `id = 1` | Imprime la canción base y su derivada anidada `[62] (live)` | pasa | Recorrido del árbol |
| P07 | E2 | Operación recursiva sobre ítem hoja sin derivadas (opción 5) | `id = 62` | Mensaje: "No tiene versiones derivadas." (caso base hoja) | pasa | Caso base sin hijos |
| P08 | E2 | Operación recursiva con id inexistente (opción 5) | `id = 9999` | Mensaje: "No existe la canción con id 9999." | pasa | Control de existencia previa |
| P09 | E3 | Agregar a la colección principal hasta el tope | equipo de 6 / equivalente | El séptimo falla con excepción propia | no corrido | Previsto para E3 |
| P10 | E3 | Desapilar historial vacío | pila vacía | Excepción propia, menú sigue | no corrido | Previsto para E3 |
| P11 | E3 | Desencolar cola vacía | cola vacía | Excepción propia, menú sigue | no corrido | Previsto para E3 |
| P12 | E3 | Listar colección con el iterador | 2+ ítems | El orden coincide con las inserciones | no corrido | Previsto para E3 |
| P13 | E4 | Búsqueda lineal y binaria | nombres válidos / inválidos | Encuentra coincidencias u ordena según corresponda | no corrido | Previsto para E4 |
| P14 | E4 | Ordenar catálogo por diferentes criterios | criterios disponibles | El orden del catálogo cambia correctamente | no corrido | Previsto para E4 |
| P15 | E5 | Guardar y recuperar estado (CSV / Binario) | registros modificados | Mantiene la persistencia y detecta archivos corruptos | no corrido | Previsto para E5 |
