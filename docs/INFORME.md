# Informe del TP

## 1. Grupo y tema

- **Integrantes:** Mauricio Medina y Nicolás Randazzo.
- **Tema:** Biblioteca musical.
- **Motivo:** Elegimos música porque nos interesaba explorar cómo organizar un catálogo de canciones y sus versiones. El dataset permite trabajar con búsquedas, ordenamientos y relaciones entre canciones. También ofrece ejemplos concretos para recorrer relaciones recursivamente, como versiones en vivo, covers y remixes. El tema conecta las estructuras de datos del curso con una aplicación conocida. El catálogo se carga desde archivos de datos y no está hardcodeado en el programa.

## 2. Modelo

Cada canción es una instancia inmutable de `Cancion`, con `id`, `titulo`, `artista`, `album`, `genero`, `anio` y `duracion_seg`. La clase es inmutable (`dataclass(frozen=True)`); las operaciones de modificación reemplazan el objeto en la colección por una nueva instancia. El catálogo que usa el CLI es una lista Python de canciones. La colección auxiliar es una `ListaEnlazada`; el historial es una `Pila` y la cola de reproducción una `Cola`, ambas construidas sobre la lista enlazada.

`BibliotecaMusical` carga canciones en un diccionario indexado por ID y las relaciones de `versiones.csv` en un diccionario que agrupa por `version_de_id`. Así, `cancion_id` identifica la canción derivada y `version_de_id` su base. El dataset seleccionado es `data/canciones.csv` junto con `data/versiones.csv`.

## 3. Recursión (E2)

La operación principal es `BibliotecaMusical.derivadas_de(cancion_id, visitadas)`. El caso base se cumple si el ID ya está en `visitadas` (evita ciclos) o si no hay versiones asociadas. En el caso recursivo, cada versión directa se agrega al resultado y se recorren las derivadas de su `cancion_id`.

Ejemplo del dataset para ID 1:

1. `derivadas_de(1, None)` registra el ID 1 y encuentra la versión 62.
2. `derivadas_de(62, {1})` registra el ID 62; como no tiene derivadas, retorna una lista vacía.
3. La primera llamada retorna la versión 62 como derivada de la canción 1.

La complejidad es O(V + E) en el subgrafo alcanzable, donde V son canciones visitadas y E relaciones recorridas; el conjunto `visitadas` y la lista de resultado usan O(V) espacio en el peor caso.

## 4. TADs (E3)

| TAD | Operaciones relevantes | Invariante / comportamiento |
| --- | --- | --- |
| `ListaEnlazada` | insertar al inicio/final, insertar ordenado, buscar, eliminar, iterar | `_longitud` coincide con el número de nodos alcanzables desde `_cabeza`. |
| `Pila` | apilar, ver tope, desapilar | LIFO; la cabeza de la lista enlazada representa el tope. |
| `Cola` | encolar, ver frente, desencolar | FIFO; se inserta al final y se extrae de la cabeza. |

La colección auxiliar se muestra mediante el iterador de `ListaEnlazada`. La pila y la cola también exponen iteradores, aunque el CLI opera mediante sus operaciones específicas.

## 5. Complejidad (E4)

Sea n la cantidad de canciones, y m la cantidad de nodos de una estructura enlazada.

| Operación | Tiempo | Espacio auxiliar | Justificación |
| --- | --- | --- | --- |
| Listar catálogo | O(n) | O(1) | Se visita cada canción una vez y se imprime directamente. |
| Búsqueda lineal | O(n) | O(1) | En el peor caso recorre todo el catálogo. |
| Búsqueda binaria | O(log n) | O(1) | Reduce a la mitad el intervalo; requiere orden por título. |
| Ordenamiento por selección | O(n²) | O(1) | Busca el mínimo del tramo restante en cada iteración. |
| Ordenamiento por inserción | O(n²) peor caso; O(n) mejor caso | O(1) | Desplaza elementos para insertar cada canción en su posición. |
| Buscar ID para ABM | O(n) | O(1) | Recorre la lista hasta localizar el ID. |
| Insertar al final de `ListaEnlazada` | O(m) | O(1) | Recorre la lista porque no mantiene una referencia al último nodo. |
| Apilar / desapilar en cabeza | O(1) | O(1) | La cabeza representa el tope. |
| Encolar | O(m) | O(1) | La inserción al final recorre la lista. |
| Desencolar | O(1) | O(1) | Se elimina la cabeza. |
| Actualizar registro binario por posición | O(1) para ubicarlo | O(1) | `seek` calcula el desplazamiento usando header y tamaño fijo. |
| Guardar/cargar catálogo | O(n) | O(n) al cargar | Se procesa cada registro una vez. |

La búsqueda binaria solo es válida si la colección está ordenada según la misma clave usada para comparar. El CLI habilita esa búsqueda después de ordenar por título.

## 6. Persistencia (E5)

El catálogo de texto se guarda en `data/canciones.csv`, con encabezado y una canción por fila. El CLI inicializa el catálogo desde ese archivo; por eso las altas, modificaciones y bajas persistidas se conservan al reiniciar.

El archivo binario usa `struct.Struct("<I 30s 25s 30s 12s 2H")`: ID como entero sin signo de 4 bytes; título de 30 bytes; artista de 25 bytes; álbum de 30 bytes; género de 12 bytes; año y duración como enteros sin signo de 2 bytes cada uno. El registro ocupa **105 bytes**. Los textos se codifican en UTF-8 y se rellenan con bytes nulos hasta alcanzar el ancho fijo; los valores que exceden el ancho se recortan.

El header usa `struct.Struct("<4s 1s I")` y ocupa **9 bytes**: magia `AYED` (4 bytes), tema `M` (1 byte) y cantidad de registros (4 bytes). El registro de posición p empieza en el desplazamiento `9 + p * 105`. La modificación abre el archivo en modo `r+b`, hace `seek` a ese desplazamiento y sobrescribe un único registro. El alta agrega un registro y actualiza la cantidad del header; la baja reescribe los registros restantes.

La capa de persistencia detecta errores de header, magia/tema incorrectos y datos truncados durante la carga. El archivo `.bin` es un artefacto generado por el programa y no se incluye en el repositorio.

## 7. Reparto de trabajo (E6)

| Integrante | Responsabilidades registradas | Temas a poder defender |
| --- | --- | --- |
| Mauricio Medina | Revisión de estructura y flujo, documentación, pruebas de regresión y ajustes de cierre E6. | Catálogo, recursión, TADs, complejidad, persistencia y protocolo. |
| Nicolás Randazzo | Implementación de la lógica del dominio, recursión, TADs y menú; persistencia de E5. | Dominio, lista enlazada, pila/cola, recursión, CLI y archivos. |

El reparto describe las responsabilidades del trabajo en equipo y no reemplaza la revisión individual del código por parte de ambos integrantes.
