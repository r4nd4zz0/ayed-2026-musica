# Informe del TP

Completar y hacer crecer en cada entrega. No hace falta prosa larga: oraciones claras y tablas.

## 1. Grupo y tema

- Tema: Biblioteca Musical
- Por qué lo eligieron (5–8 líneas): Puramente por interés. A ninguno de los dos nos interesaba un recetario o una pokedex, mientras que si no interesaba ver como sería la biblioteca musical.

## 2. Modelo

Qué es un ítem del catálogo. Qué es mutable y qué no (E1). Cómo se relacionan catálogo, colección principal, pila y cola.

Un ítem del catálogo es una instancia de la clase inmutable "Canción" ("id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"). Las relaciones jerárquicas se representan mediante la clase inmutable "VersionCancion" ("cancion_id", "version_de_id", "tipo"), donde "version_de_id" referencia al ID de la canción base. Ambas entidades están implementadas con "@dataclass(frozen=True)" garantizando inmutabilidad. La clase "BibliotecaMusical" administra el catálogo en memoria mediante dos diccionarios:

* "canciones": asocia cada ID con su objeto "Cancion".
* "versiones_por_base": agrupa bajo el ID de la canción base una lista con todas sus versiones derivadas directas.

## 3. Recursión (E2)

- Función: BibliotecaMusical.derivadas_de(cancion_id: int, visitadas: set[int] | None = None) -> list[VersionCancion]
- Caso base: Si "cancion_id in visitadas" detecta referencias circulares, retorna una lista vacía ("[]") inmediatamente, cortando la ejecución para prevenir ciclos infinitos. Si la canción no tiene versiones derivadas registradas, el bucle for no se ejecuta y la función retorna directamente "resultado = []".
- Caso recursivo: Para cada versión directa asociada a "cancion_id", se añade dicha versión al resultado y se invoca "derivadas_de(version.cancion_id, visitadas)" para acumular las derivaciones de los niveles inferiores.
- Traza de un ejemplo real del dataset: Búsqueda de versiones derivadas para la canción base ID 1:
	* "derivadas_de(1, None)": visitadas pasa a ser "{1}". Encuentra una derivada directa: la canción 62 ("live"). La agrega a la lista e invoca "derivadas_de(62, {1})".
	* "derivadas_de(62, {1})": visitadas pasa a ser "{1, 62}". Como la canción 62 no tiene derivadas en el catálogo, el bucle no realiza llamadas hijas y retorna "[]".
	* Resolución: La primera llamada recibe "[]", consolida su lista final con "[VersionCancion(62, 1, 'live')]" y la retorna.

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada |  |  |
| Pila |  |  |
| Cola |  |  |

Dónde se usa cada uno en el dominio.

## 5. Complejidad (E4)

| Operación | Tiempo | Espacio | Por qué |
| --- | --- | --- | --- |
|  |  |  |  |

Mediciones (`time.perf_counter`):

| Operación | n | segundos |
| --- | --- | --- |
|  |  |  |

## 6. Persistencia (E5)

- Layout del registro binario (campos, `struct`, anchos):
- Header:
- Cómo se actualiza un registro por posición:

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
|  |  |  |
