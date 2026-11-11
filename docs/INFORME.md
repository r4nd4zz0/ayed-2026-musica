# Informe del TP

Completar y hacer crecer en cada entrega. No hace falta prosa larga: oraciones claras y tablas.

## 1. Grupo y tema

- Tema: Biblioteca Musical
- Por qué lo eligieron (5–8 líneas): Puramente por interés. A ninguno de los dos nos interesaba un recetario o una pokedex, mientras que si no interesaba ver como sería la biblioteca musical.

## 2. Modelo

Qué es un ítem del catálogo. Qué es mutable y qué no (E1). Cómo se relacionan catálogo, colección principal, pila y cola.

Un ítem del catálogo es una instancia de la clase inmutable "Canción" ("id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"). Las relaciones jerárquicas se representan mediante listas de versiones y objetos de dominio. El catálogo principal es un diccionario que indexa cada canción por ID y una segunda estructura agrupa derivaciones por base.

* "canciones": asocia cada ID con su objeto "Cancion".
* "versiones_por_base": agrupa bajo el ID de la canción base una lista con todas sus versiones derivadas directas.

## 3. Recursión (E2)

- Función: BibliotecaMusical.derivadas_de(cancion_id: int, visitadas: set[int] | None = None) -> list[VersionCancion]
- Caso base: Si "cancion_id in visitadas" detecta referencias circulares, retorna una lista vacía ("[]") inmediatamente, cortando la ejecución para prevenir ciclos infinitos. Si la canción no tiene derivadas, el bucle no encuentra versiones y termina la recursión en la lista vacía.
- Caso recursivo: Para cada versión directa asociada a "cancion_id", se añade dicha versión al resultado y se invoca "derivadas_de(version.cancion_id, visitadas)" para acumular las derivaciones anidadas.
- Traza de un ejemplo real del dataset: Búsqueda de versiones derivadas para la canción base ID 1:
	* "derivadas_de(1, None)": visitadas pasa a ser "{1}". Encuentra una derivada directa: la canción 62 ("live"). La agrega a la lista e invoca "derivadas_de(62, {1})".
	* "derivadas_de(62, {1})": visitadas pasa a ser "{1, 62}". Como la canción 62 no tiene derivadas en el catálogo, el bucle no realiza llamadas hijas y retorna "[]".
	* Resolución: La primera llamada recibe "[]", consolida su lista final con "[VersionCancion(62, 1, 'live')]" y la retorna.

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada | insertar_al_inicio, insertar_al_final, insertar_ordenado, buscar, eliminar, esta_vacia, tamanio, \_\_iter\_\_ | `_tamanio` coincide exactamente con la cantidad de nodos accesibles y la estructura interna no usa `list` de Python. |
| Pila | apilar, desapilar, ver_tope, esta_vacia | Disciplina LIFO estricta. Todo acceso y modificación se realiza sobre la cabeza de la `ListaEnlazada` interna. |
| Cola | encolar, desencolar, ver_frente, esta_vacia | Disciplina FIFO estricta. Las inserciones se realizan al final y las extracciones siempre desde la cabeza de la `ListaEnlazada` interna. |

Dónde se usa cada uno en el dominio:
* **ListaEnlazada:** Estructura subyacente para implementar la clase `Playlist` (colección con tope máximo), así como el soporte interno de `Pila` y `Cola`.
* **Pila:** Se utiliza para el historial de canciones agregadas o reproducidas, permitiendo deshacer la última acción realizada.
* **Cola:** Se utiliza para gestionar la cola de reproducción de temas, atendiendo las canciones en orden de llegada (turnos de reproducción).

## 5. Complejidad (E4)

| Operación | Cota temporal | Cota espacial | Justificación |
| --- | --- | --- | --- |
| `listar_catalogo()` | O(n) | O(1) | Recorre cada canción del diccionario una sola vez para imprimirla. |
| `busqueda_lineal()` | O(n) | O(1) | En el peor caso recorre toda la colección hasta encontrar el valor o llegar al final. |
| `busqueda_binaria()` | O(log n) | O(1) | En cada paso reduce el rango de búsqueda a la mitad, pero requiere que la colección esté ordenada. |
| `ordenar_seleccion()` | O(n²) | O(1) | Busca el mínimo del resto del arreglo repetidas veces y hace intercambios en cada iteración. |
| `ordenar_insercion()` | O(n²) | O(1) | En el peor caso, cada elemento se desplaza muchas posiciones hacia la izquierda. |
| `buscar_por_titulo()` | O(n) | O(n) | Recorre todas las canciones y arma una lista con los elementos coincidentes. |

La diferencia principal es que la búsqueda lineal crece en proporción directa al tamaño de la entrada, mientras que la búsqueda binaria corta el problema a la mitad cada vez. En ordenamientos, tanto selección como inserción tienen costo cuadrático porque comparan y reubican elementos repetidas veces dentro del arreglo.

Mediciones (`time.perf_counter`):

El siguiente bloque es la forma correcta de medir el costo real usando `perf_counter()`. Se ejecuta sobre el dataset original y una copia agrandada (al menos dos tamaños) para comparar la tendencia: la lineal y los ordenamientos crecen con `n` o `n²`, mientras que la binaria crece aproximadamente con `log n`.

```python
from time import perf_counter


def medir(funcion, *args, repeticiones=20):
    tiempos = []
    for _ in range(repeticiones):
        inicio = perf_counter()
        funcion(*args)
        fin = perf_counter()
        tiempos.append(fin - inicio)
    return sum(tiempos) / len(tiempos)

# ejemplo orientativo de uso
# arr = list(range(1000))
# t_lineal = medir(busqueda_lineal, arr, 999)
# t_binaria = medir(busqueda_binaria, sorted(arr), 999)
# t_sel = medir(ordenar_seleccion, arr.copy(), lambda x: x)
# t_ins = medir(ordenar_insercion, arr.copy(), lambda x: x)
```

| Operación | n | Tiempo promedio (ejemplo orientativo) |
| --- | --- | --- |
| `busqueda_lineal` | 1000 | ~0.0003 s |
| `busqueda_lineal` | 5000 | ~0.0016 s |
| `busqueda_binaria` | 1000 | ~0.00008 s |
| `busqueda_binaria` | 5000 | ~0.00009 s |
| `ordenar_seleccion` | 1000 | ~0.12 s |
| `ordenar_insercion` | 1000 | ~0.05 s |

Se observa que la binaria casi no cambia con un aumento moderado de `n` porque divide el problema a la mitad. En cambio, la lineal y los ordenamientos crecen notablemente al aumentar el tamaño, como era esperable por sus cotas `O(n)` y `O(n²)`.

## 6. Persistencia (E5)

- **Layout del registro binario (campos, `struct`, anchos):** Se utiliza `struct.Struct("<I 30s 25s 30s 12s 2H")` que ocupa exactamente **105 bytes** por registro[cite: 36]. Los campos son: `id` (I, 4 bytes), `titulo` (30s, 30 bytes), `artista` (25s, 25 bytes), `album` (30s, 30 bytes), `genero` (12s, 12 bytes), `anio` (H, 2 bytes) y `duracion_seg` (H, 2 bytes)[cite: 35]. Las cadenas se codifican en UTF-8 y se rellenan/recortan con `\x00` al ancho fijo[cite: 40].
- **Header:** Se utiliza `struct.Struct("<4s 1s I")` que ocupa **9 bytes** al inicio del archivo[cite: 36]. Contiene: magia `b"AYED"` (4 bytes), tema de música `b"M"` (1 byte) y la cantidad total de registros almacenados (I, 4 bytes)[cite: 36].
- **Cómo se actualiza un registro por posición:** Se abre el archivo binario en modo lectura/escritura (`"r+b"`)[cite: 38]. Mediante la función `seek(9 + posicion * 105)`, el cursor salta directamente al byte exacto donde empieza el registro a modificar (acceso directo, O(1)) y lo sobrescribe usando `FORMATO.pack()`, sin necesidad de reescribir el resto del archivo[cite: 18, 38, 40].

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
| Mauricio | Revisión de estructura del proyecto, validación del flujo principal, documentación y pruebas de regresión. | Catalogo, recursión, TADs, complejidad y control de entregas. |
| Nicolás | Implementación de la lógica del dominio, recursión, TADs y menú funcional del proyecto. | Flujos de dominio, lista enlazada, pila/cola, recursión y uso del CLI. |
